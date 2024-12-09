import asyncio
from datetime import datetime
from app.services.llm_service import process_log_with_rag
from app.utils.helpers import process_rag_response, update_rag_response_on_cloud

async def process_log(log_data, application_id: str, log_id: str, app):
    """
    Process the log using the RAG module, retrying up to 5 times if the RAG response is empty.

    Args:
        log_data (dict): The log data to process.
        application_id (str): The application ID.
        log_id (str): The log ID.
        app (FastAPI): The FastAPI app instance to access state.

    Returns:
        dict: The response from processing the log.
    """
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            # Await the asynchronous function
            response = await process_log_with_rag(log_data,log_id, application_id, app)
            rag_response = response.get("rag_response", "")

            if rag_response:
                formatted_rag_response = process_rag_response(rag_response)
                update_rag_response_on_cloud(
                    log_id=log_id,
                    application_id=application_id,
                    rag_response={
                        "formatted_rag_response": formatted_rag_response,
                        "rag_response": response,
                        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )
                print(f"Attempt {attempt}: Successfully processed log.")
                return response
            else:
                print(f"Attempt {attempt}: RAG response is empty. Retrying...")
                await asyncio.sleep(1)  # Optional: wait before retrying
        except Exception as e:
            print(f"Attempt {attempt}: Error processing log: {str(e)}")
            await asyncio.sleep(1)

    print("Failed to process log after multiple attempts.")
    return {"error": "Failed to process log after multiple attempts."}
