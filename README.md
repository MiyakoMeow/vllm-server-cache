# vLLM 本地推理服务

基于 vLLM 的 Qwen3.5-2B Q4_K_M 量化模型推理服务，提供 OpenAI 兼容接口。

## 环境要求

- **Python**: 3.10+
- **GPU**: NVIDIA CUDA (RTX 2080 8GB 可用)
- **vLLM**: 0.19.0 (最新 stable)

## 模型信息

- **模型**: [unsloth/Qwen3.5-2B-GGUF](https://huggingface.co/unsloth/Qwen3.5-2B-GGUF)
- **量化版本**: Q4_K_M
- **文件**: `qwen3.5-2b-q4_k_m.gguf`
- **大小**: ~1.3 GB

## 快速启动

### 1. 安装依赖

```bash
uv sync
```

### 2. 启动服务

```bash
uv run vllm serve unsloth/Qwen3.5-2B-GGUF \
    --port 50721 \
    --tensor-parallel-size 1 \
    --model qwen3.5-2b-q4_k_m.gguf
```

### 3. 验证服务

```bash
curl http://localhost:50721/v1/models
```

## API 使用

服务启动后，可通过 OpenAI 兼容接口调用：

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

## 常用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--port` | 服务端口 | 8000 |
| `--tensor-parallel-size` | GPU 并行数量 | 1 |
| `--max-model-len` | 最大上下文长度 | 32768 |
| `--gpu-memory-utilization` | GPU 显存利用率 | 0.9 |
