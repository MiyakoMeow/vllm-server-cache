"""vLLM 本地推理服务启动脚本生成器."""

import socket
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ModelConfig:

    """模型配置."""

    name: str
    gguf_file: str | None = None


MODELS: dict[str, ModelConfig] = {
    "qwen3.5-2b-q4km": ModelConfig(
        name="unsloth/Qwen3.5-2B-GGUF",
        gguf_file="qwen3.5-2b-q4_k_m.gguf",
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


def generate_script(model: str, port: int, gguf_file: str | None) -> str:
    """生成启动脚本."""
    model_arg = f'--model "{gguf_file}"' if gguf_file else model
    lines = [
        "#!/bin/bash",
        f"# vLLM 启动脚本 - 模型: {model}",
        "",
        f"if ! nc -z localhost {port} 2>/dev/null; then",
        "    echo ''",
        f"    echo '正在启动 vLLM 服务 on port {port}...'",
        "    echo ''",
        f"    vllm serve {model_arg} \\",
        f"        --port {port} \\",
        "        --tensor-parallel-size 1 \\",
        "        --gpu-memory-utilization 0.9",
        "    echo ''",
        f"    echo 'vLLM 服务已停止 (端口 {port})'",
        "else",
        "    echo ''",
        f"    echo '错误: 端口 {port} 已被占用!'",
        "    exit 1",
        "fi",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    model_key = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL

    if model_key not in MODELS:
        sys.exit(1)

    config = MODELS[model_key]

    if not check_port(PORT):
        sys.exit(1)

    script = generate_script(config.name, PORT, config.gguf_file)
    Path("run.sh").write_text(script, encoding="utf-8")

