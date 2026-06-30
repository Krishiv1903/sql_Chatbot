import ollama
import json
import re
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()

def parse_message_with_llm(message: str):
    today = date.today().strftime("%Y-%m-%d")

    prompt = f"""
You are a strict JSON extraction engine.

CONTEXT:
- Today is {today} or Date month year(23 January 2023) or DD/MM/YYYY
- Accept formats:
  • "23 January 2023"
  • "23/01/2023"
  • natural language ("tomorrow", "next monday")
- Convert all date expressions into YYYY-MM-DD format
- Convert 1 pm to 13:00, 3 am to 03:00
- Accepted format for time: 
  • "XX am"
  • "XX pm"
- Convert all time expressions into HH:MM:SS format 


TASK:
Extract structured data from the message.


FIELDS:
- intent:
  "create" → booking/scheduling
  "get" → viewing/listing appointments
- name:
  person name (1-2 words only)
- date:
  single date (YYYY-MM-DD)'
- time:
  time in HH:MM format
- start_date:
  used ONLY for range queries
- end_date:
  used ONLY for range queries
- description:
  short purpose (1-3 words only)


RULES:
- "between X and Y" → populate start_date AND end_date
- description MUST NOT be:
  "booking", "appointment", "meeting", "schedule"
- description must be meaningful:
  examples: "dentist", "lunch", "interview"
- Return ONLY valid JSON
- No explanations, no comments, no extra text
- Missing fields must be null


FORMAT:
{{
  "intent": "",
  "name": null,
  "date": null,
  "time": null,
  "start_date": null,
  "end_date": null,
  "description": null
}}

MESSAGE:
"{message}"
"""

    response = ollama.chat(
      # llama3 / qwen3:8b
      model="llama3",
      messages=[{"role": "user", "content": prompt}]
    )
    # ollama pull qwen3:8b
    # ollama pull llama3


    content = response["message"]["content"]
    print("RAW:", content)

    content = re.sub(r"//.*", "", content)

    start = content.find("{")
    end = content.rfind("}")

    if start == -1:
        return None

    if end == -1:
        content += "}"
        end = len(content) - 1

    try:
        return json.loads(content[start:end + 1])
    except:
        return None
    
