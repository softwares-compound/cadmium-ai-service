from app.services.llm_service import query_llm

def process_log(log_data):
    # Extract the message or error field from the log
    message = log_data.get("error", "No error message")[:40] + "..." if len(log_data.get("error", "")) > 40 else log_data.get("error", "No error message")
    print(f"Processing Log: {message}")

    # Query the local LLM with the log message
    # llm_response = query_llm(message)
    # print(f"LLM Response: {llm_response}")
