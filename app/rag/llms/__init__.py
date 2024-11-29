from .ollama import ollama_llm
from .openai import openai_llm
from app.core.config import settings


if settings.preferred_environment == "local":
    llm = ollama_llm
else:
    llm = openai_llm

