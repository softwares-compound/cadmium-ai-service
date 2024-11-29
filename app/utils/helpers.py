import requests
from app.core.config import API_BASE_URL, WEBSOCKET_HEADERS

def update_rag_response_on_cloud( log_id, rag_response, application_id):
    """
    Updates the rag_response of a log on the Rust API.

    Args:
        base_url (str): The base URL of the Rust API.
        log_id (str): The ID of the log to update.
        rag_response (str): The RAG response to update in the log.
        headers (dict): Headers for authentication, including CD-ID, CD-Secret, and Application-ID.

    Returns:
        dict: The API response.
    """
    try:
        # Endpoint for updating the RAG inference
        url = f"{API_BASE_URL}/logs/{log_id}/rag-inference"

        # Prepare the payload
        payload = {
            "rag_response": rag_response
        }
        headers = {
            **WEBSOCKET_HEADERS,
            "Application-ID": application_id
        }
        # Make the PUT request
        response = requests.put(url, json=payload, headers=headers)

        # Check for HTTP errors
        response.raise_for_status()

        # Return the JSON response
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Failed to update rag_response: {str(e)}")
        return {"error": str(e)}


def process_rag_response(rag_response: str) -> list:
    """
    Splits the RAG response into an array of dictionaries with separate
    markdown and code parts, ensuring only actual code content is extracted
    without language specifiers like `bash` or `python`.

    Args:
        rag_response (str): The RAG response containing text and code.

    Returns:
        list: A list of dictionaries where each dictionary represents either
              a markdown text or a code block.
    """
    import re

    # Define a regex pattern to identify code blocks (removing language specifiers)
    code_block_pattern = r"```(?:\w+)?\n(.*?)```"

    # Find all code blocks and their positions
    matches = list(re.finditer(code_block_pattern, rag_response, re.DOTALL))

    response_parts = []
    cursor = 0

    for match in matches:
        start, end = match.span()

        # Extract the markdown text before the code block
        if cursor < start:
            markdown_text = rag_response[cursor:start].strip()
            if markdown_text:
                response_parts.append({"type": "markdown", "value": markdown_text})

        # Extract the code block itself, stripping unnecessary language specifiers
        code_text = match.group(1).strip()
        response_parts.append({"type": "code", "value": code_text})

        # Move the cursor past the code block
        cursor = end

    # Add any remaining markdown text after the last code block
    if cursor < len(rag_response):
        markdown_text = rag_response[cursor:].strip()
        if markdown_text:
            response_parts.append({"type": "markdown", "value": markdown_text})

    return response_parts
