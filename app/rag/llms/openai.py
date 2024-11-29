from llama_index.llms.openai import OpenAI

from app.core.config import settings
model_kwargs = {
    "openai_api_key": settings.openai_api_key,
    "openai_model_name": settings.openai_model_name,
}

openai_llm = OpenAI(**model_kwargs)
