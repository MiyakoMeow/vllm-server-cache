"""vLLM 本地推理服务启动脚本生成器."""

import argparse
import logging
import socket
import sys
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    """模型配置."""

    name: str
    tokenizer: str | None = None
    hf_config_path: str | None = None
    tensor_parallel_size: int | None = None
    gpu_memory_utilization: float | None = None


MODELS: dict[str, ModelConfig] = {
    "qwen3.5-2b-q4km": ModelConfig(
        name="Qwen/Qwen3.5-2B",
        tokenizer="Qwen/Qwen3.5-2B",
    ),
}

DEFAULT_MODEL = "qwen3.5-2b-q4km"
DEFAULT_GPU_MEMORY_UTILIZATION = 0.75
PORT = 50721


def check_port(port: int) -> bool:
    """检查端口是否可用."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("", port))
        except OSError:
            return False
    return True


def generate_script(config: ModelConfig, port: int) -> str:
    """生成启动脚本."""
    model_arg = f'"{config.name}"'
    parts = [f"uv run vllm serve {model_arg}"]
    if config.tokenizer:
        parts.append(f"--tokenizer {config.tokenizer}")
    if config.hf_config_path:
        parts.append(f"--hf-config-path {config.hf_config_path}")
    parts.append(f"--port {port}")
    if config.tensor_parallel_size is not None:
        parts.append(f"--tensor-parallel-size {config.tensor_parallel_size}")
    if config.gpu_memory_utilization is not None:
        parts.append(f"--gpu-memory-utilization {config.gpu_memory_utilization}")
    return f"#!/bin/bash\n{' '.join(parts)}\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成 vLLM 启动脚本")
    parser.add_argument("model", nargs="?", default=DEFAULT_MODEL, help="模型 key")
    parser.add_argument(
        "--gpu-memory-utilization",
        type=float,
        default=DEFAULT_GPU_MEMORY_UTILIZATION,
        help="GPU 显存利用率 (0-1)",
    )
    parser.add_argument("--tensor-parallel-size", type=int, help="Tensor 并行度")
    parser.add_argument("--port", type=int, default=PORT, help="服务端口")
    args = parser.parse_args()

    if args.model not in MODELS:
        sys.exit(1)

    config = MODELS[args.model]
    if args.gpu_memory_utilization is not None:
        config.gpu_memory_utilization = args.gpu_memory_utilization
    if args.tensor_parallel_size is not None:
        config.tensor_parallel_size = args.tensor_parallel_size

    if not check_port(args.port):
        sys.exit(1)

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    script = generate_script(config, args.port)
    Path("run.sh").write_text(script, encoding="utf-8")
    logger.info("启动命令已写入 run.sh:\n%s", script)
