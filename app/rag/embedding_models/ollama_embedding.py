from llama_index.embeddings.ollama import OllamaEmbedding
from app.core.config import settings

ollama_embedding = OllamaEmbedding(
    model_name=settings.local_embedding_model or "nomic-embed-text:latest",
    base_url="http://localhost:11434",
)