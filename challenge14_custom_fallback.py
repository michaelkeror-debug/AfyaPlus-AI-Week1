import os
import time
from dotenv import load_dotenv
from openai import OpenAI, APITimeoutError, RateLimitError, APIError

load_dotenv()
client = OpenAI()

BLOCKED_PATTERNS = [
    "you have", # Implies diagnosis
    "you should take", # Implies prescription
    "diagnosis",
    "prescribe",
    "mg", # Medication dosage
]

FALLBACK_TIMEOUT = (
    "Our system is responding slowly right now. Please try again in a moment. "
    "If urgent, call our helpline at +254-XXX-XXXX."
)
FALLBACK_RATE_LIMIT = (
    "Our service is busy at the moment. Please wait one minute and try again."
)
FALLBACK_API_ERROR = (
    "We could not process your request. Please contact our helpline at "
    "+254-XXX-XXXX or visit your nearest healthcare facility."
)
FALLBACKS = {
    "timeout":    FALLBACK_TIMEOUT,
    "rate_limit": FALLBACK_RATE_LIMIT,
    "api_error":  FALLBACK_API_ERROR,}

def validate_response(response_text):
    lowered = response_text.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern in lowered:
            return False, f"Blocked: contains '{pattern}'"
    return True, "Passed"

def get_ai_response(patient_message, max_retries=3):
    last_error = "api_error"
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are AfyaPlus Health Assistant. Provide safe, general health guidance. Never diagnose or prescribe."},
                    {"role": "user", "content": patient_message}
                ],
                temperature=0.3,
                max_tokens=200,
                timeout=10.0
            )
            ai_text = response.choices[0].message.content
            is_safe, _ = validate_response(ai_text)
            return ai_text if is_safe else FALLBACK_API_ERROR
        except APITimeoutError:
            last_error = "timeout"
            time.sleep(2 ** attempt)
        except RateLimitError:
            last_error = "rate_limit"
            time.sleep(5 * (attempt + 1))
        except APIError:
            last_error = "api_error"
    return FALLBACKS[last_error]

print("--- Production Pipeline Test ---")
test_messages = [
    "I have a mild headache today",
    "My chest hurts and I cannot breathe properly",
]
for msg in test_messages:
    print(f"Patient: {msg}")
    response = get_ai_response(msg)
    print(f"Assistant: {response}")
    print()