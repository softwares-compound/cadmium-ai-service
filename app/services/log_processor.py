import requests
from app.core.config import settings
from app.services.llm_service import query_llm

def process_log(log):
    # Fetch additional data if necessary
    response = requests.get(f"{settings.cadmium_cloud_api_url}/logs/{log.id}")
    log_data = response.json()
    
    # Process log with LLM
    llm_response = query_llm(log_data['message'])
    return llm_response
