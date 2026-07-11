import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
cloud_client = OpenAI()
local_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

SYSTEM_PROMPT = "You are a health assistant. Provide brief, safe guidance."
patient_message = "I have chest pain when I breathe deeply"

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": patient_message}
]
