import os
import sys
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    print("ERROR: OPENAI_API_KEY missing. Did you create the .env file?")
    sys.exit(1)

if api_key == "sk-your-key-here":
    print("ERROR: Placeholder key detected. Replace 'sk-your-key-here' with your real key.")
    sys.exit(1)

masked = api_key[:7] + "..." + api_key[-4:]
print(f"Key loaded successfully: {masked}")
