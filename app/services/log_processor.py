from app.services.llm_service import query_llm

async def process_log(log_data):
    # Extract the message or error field from the log
    message = log_data.get("error", "No error message")

    # Query the local LLM with the log message
    llm_response = await query_llm(message)  #
    print(f"LLM Response: {llm_response}")
