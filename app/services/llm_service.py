import requests

async def query_llm(message: str):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen2.5-coder:latest",
        "prompt": generate_prompt(message),
        'stream': False,
        "options": {
            "temperature": 0.7,
            "max_tokens": 150
        }
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("response", "")


def generate_prompt(log_message) -> str:
    prompt = f"""
You are an expert in analyzing error logs and providing detailed explanations and solutions. 
Analyze the following log entry:



### Your Task:
1. Identify the **root cause** of the issue based on the log message.
2. Suggest a **clear and concise solution** or steps to resolve the error.
3. If additional context or debugging information is needed, provide a list of **questions to gather more details**.
4. Summarize your findings and solution in a structured and developer-friendly way.

Ensure that your explanation and solution are **specific, actionable**, and **suitable for a software engineer**.

### Output Format:
**Root Cause**: <Describe the root cause>
**Solution**: <Provide actionable steps to resolve the issue>
**Additional Questions (if any)**: <List any clarifying questions>
**Summary**: <Summarize your analysis in one concise paragraph>

Here's the log entry:
"""
    return prompt + log_message
