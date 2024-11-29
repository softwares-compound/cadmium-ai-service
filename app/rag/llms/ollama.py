from llama_index.llms.ollama import Ollama

from app.core.config import settings

model_kwargs = {
    "model_path": settings.local_llm_endpoint,
    "model": settings.local_llm_model or "qwen2.5-coder:latest",
    "additional_kwargs":{"options": {"num_ctx": 32768}},
}

ollama_llm = Ollama(**model_kwargs)
