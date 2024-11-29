from .ollama_embedding import ollama_embedding
from app.core.config import settings

if settings.preferred_environment == "local":
    embedding = ollama_embedding