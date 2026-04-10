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

# 生成启动脚本
uv run python main.py

# 启动服务
./run.sh
```

## 拓展模型

在 `main.py` 的 `MODELS` 字典中添加新模型：

```python
MODELS: dict[str, ModelConfig] = {
    "qwen3.5-2b-q4km": ModelConfig(
        name="unsloth/Qwen3.5-2B-GGUF",
        gguf_file="qwen3.5-2b-q4_k_m.gguf",
        tensor_parallel_size=1,
        gpu_memory_utilization=0.9,
    ),
}
```

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
- 架构: Turing (SM 7.5) ✅ 支持 GGUF
