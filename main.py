"""vLLM 本地推理服务启动脚本生成器."""

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
        name="unsloth/Qwen3.5-2B-GGUF:Q4_K_M",
        tokenizer="Qwen/Qwen3.5-2B",
        hf_config_path="Qwen/Qwen3.5-2B",
    ),
}

DEFAULT_MODEL = "qwen3.5-2b-q4km"
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
    model_key = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL

    if model_key not in MODELS:
        sys.exit(1)

    config = MODELS[model_key]

    if not check_port(PORT):
        sys.exit(1)

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    script = generate_script(config, PORT)
    Path("run.sh").write_text(script, encoding="utf-8")
    logger.info("启动命令已写入 run.sh:\n%s", script)
