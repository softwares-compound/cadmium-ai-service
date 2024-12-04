from datetime import datetime
from fastapi import HTTPException
from llama_index.core.base.response.schema import Response

def process_log_with_rag(log_data: dict, application_id: str, app):
    """
    Process log data using NaiveRAGService to find a solution.

    Args:
        app (FastAPI): The FastAPI application instance to access app state.
        log_data (dict): The structured log data containing details like error, traceback, and other metadata.
        application_id (str): The application ID to fetch the appropriate NaiveRAGService.

    Returns:
        dict: The response from the RAG service with additional metadata.
    """
    try:
        # Get the appropriate NaiveRAGService from app state
        rag_service = app.state.naive_rag_services.get(application_id)
        if not rag_service:
            raise HTTPException(
                status_code=404,
                detail=f"RAG service for application ID '{application_id}' not found.",
            )

        # Extract relevant information from the log data
        error_message = log_data.get("error", "No error message provided.")
        traceback = log_data.get("traceback", "No traceback available.")
        url = log_data.get("url", "No URL provided.")
        method = log_data.get("method", "No method provided.")
        created_at = log_data.get("created_at", "No timestamp provided.")

        # Construct the query for the RAG service
        query = f"""
        I encountered the following error while accessing {url} using {method} method:
        Error Message: {error_message}
        Traceback: {traceback}
        Can you provide a detailed solution or suggest debugging steps?
        """

        # Query the RAG service
        response: Response = rag_service.query(query)
        print(f"RAG response: {response}")

        # Prepare a structured response
        print(f"Type of application_id: {type(application_id)}")
        print(f"Type of created_at: {type(created_at)}")
        print(f"Type of query: {type(query)}")
        print(f"Type of response: {type(response)}")
        print(f"Type of processed_at: {type(datetime.utcnow().isoformat() + 'Z')}")
        return {
            "application_id": application_id,
            "created_at": created_at,
            "query": query,
            "rag_response": response.response,
            "processed_at": datetime.utcnow().isoformat() + "Z",
        }

    except Exception as e:
        print(f"An error occurred while processing the log: {str(e)}")
        return {
            "error": f"An error occurred while processing the log: {str(e)}",
            "log_data": log_data,
            "processed_at": datetime.utcnow().isoformat() + "Z",
        }
