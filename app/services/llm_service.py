import requests
from app.core.config import settings

def query_llm(message: str):
    response = requests.post(settings.local_llm_endpoint, json={"message": message})
    return response.json()
