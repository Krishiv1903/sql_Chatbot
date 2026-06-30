from langchain.llms import Ollama

# initialize LLM
llm = Ollama(model="llama3")

def extract_department(message: str):
    prompt = f"""
You are a medical assistant.

Extract ONLY the department name from the message below.

Allowed departments:
dentist, cardiac, checkup, surgery, consultation, therapy,
treatment, physio, scan, xray, blood test, lab, medical

Rules:
- Return ONLY one word or phrase from the list
- No explanation
- If nothing matches, return "none"

Message:
{message}
"""

    response = llm.invoke(prompt)
    dept = response.strip().lower()
    if dept == "none":
        return None
    return dept