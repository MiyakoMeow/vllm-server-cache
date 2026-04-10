# vLLM 本地推理服务

基于 vLLM 的 Qwen3.5-2B Q4_K_M 量化模型推理服务，提供 OpenAI 兼容接口。

## 模型信息

- **模型**: [unsloth/Qwen3.5-2B-GGUF](https://huggingface.co/unsloth/Qwen3.5-2B-GGUF)
- **量化版本**: Q4_K_M
- **文件**: `qwen3.5-2b-q4_k_m.gguf`
- **大小**: ~1.3 GB

## 快速启动

```bash
# 安装依赖
uv sync

# 启动服务（自动检测端口冲突）
uv run python main.py

# 或使用自定义参数
uv run python main.py --model unsloth/Qwen3.5-2B-GGUF --port 50721 --gguf-file qwen3.5-2b-q4_k_m.gguf
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--model` | 模型名称或路径 | unsoth/Qwen3.5-2B-GGUF |
| `--gguf-file` | GGUF 文件名 | None |
| `--port` | 服务端口 | 50721 |
| `--gen-script` | 仅生成启动脚本 | False |
| `--output` | 启动脚本输出路径 | run.sh |

## 验证服务

```bash
curl http://localhost:50721/v1/models
```

## API 使用

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:50721/v1",
    api_key="EMPTY"
)

response = client.chat.completions.create(
    model="unsloth/Qwen3.5-2B-GGUF",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

## 推荐采样参数

| 场景 | temperature | top_p | top_k | presence_penalty |
|------|-------------|-------|-------|------------------|
| 文本生成 | 1.0 | 1.00 | 20 | 2.0 |
| 视觉语言 | 0.7 | 0.80 | 20 | 1.5 |

## GPU 要求

- NVIDIA GPU with CUDA support
- 推荐 8GB+ 显存 (RTX 2080 可用)
