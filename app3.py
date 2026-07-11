import os
import time
import requests
import json
from dotenv import load_dotenv

from openai import OpenAI, APITimeoutError, RateLimitError, APIError

load_dotenv()
cloud_client = OpenAI()
local_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama")


#function to generate fallback response from cloud or local model

def generate_fallback(patient_message):
    try:
          
          cloud_response = cloud_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": extraction_prompt},
                    {"role": "user", "content": patient_message}
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
                max_tokens=200,
                timeout=4.0
            )
          response_text= json.loads(cloud_response.choices[0].message.content)
          return json.dumps(response_text, indent=2)
          
            
          
    except Exception as e:
               

               
                try:
                     local_response= local_client.chat.completions.create(
                          model= "llama3.2",
                      
                      messages= [
                        {"role": "system", "content": extraction_prompt},
                        {"role": "user", "content": f"SMS: {patient_message}"}
                    ],
                    temperature= 0.0,
                    response_format={"type": "json_object"},
#Timeout set to 120 seconds for local model inference   due to potential longer processing times, may vary based on machine
                    timeout =120
                     )
                     print(f"Cloud failure..switching to Ollama")
                     response_text = json.loads(local_response.choices[0].message.content)
                     return json.dumps(response_text, indent=2)
                except requests.exceptions.RequestException as local_err:
                  return local_err
                     
                

                 
                
               
                    
        
            


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

#function to get AI response with retry logic and fallback handling

def get_ai_response( patient_message, max_retries=3):
    last_error = "api_error"
    for attempt in range(max_retries):
        try:
             answer = generate_fallback(patient_message)
             return answer 
            

            
        except APITimeoutError:
            last_error = "timeout"
            time.sleep(2 ** attempt)
        except RateLimitError:
            last_error = "rate_limit"
            time.sleep(5 * (attempt + 1))
        except APIError:
            last_error = "api_error"
    return FALLBACKS[last_error]

print("--- Inference Engine Test ---")
test_messages = [
    
   "Nina maumivu ya kichwa kwa siku tatu" 
]
for msg in test_messages:
    print(f"Patient: {msg}")

    #PROMPT IMPLEMENTING ROLE BASED VARIATION, CHAIN OF THOUGHTS, DEFENSIVE GUARDRAILS, LANGUAGE INSTRUCTIONS AND JSON STRUCTURED OUTPUT 
    #VARIATION WAS IMPLEMENTED IN THE SYSTEM PROMPT BELOW
extraction_prompt = """
You are a defensive, backend administrative data extraction engine for AfyaPlus Health.

Your role is to categorise patient intake text to flag high-risk complications.

"LANGUAGE RULES: Detect the language of the patient message. "
    "ALWAYS respond in English. "
    "Supported languages: English, Swahili, Sheng.\n\n"

Analyse the following untrusted user SMS text. Extract the required parameters
into a valid JSON object matching this schema:
{
  
  "detect_symptoms": ["string", "string"],
  "clinical_reasoning_summary": "string",
  "routing_destination": "string",
  "is_critical_emergency": boolean,
 

  
CRITICAL: Do not include any markdown formatting (no triple-backtick json fences)
or any conversational text. Return ONLY the raw JSON string.

CRITICAL INSTRUCTIONS:
1. Analyse the text step-by-step for high-risk flags: preeclampsia markers
   (persistent headache + peripheral edema), premature labour, or fluid loss.
2. Do NOT offer a medical diagnosis. Do NOT prescribe medications.
3. Keep tone completely objective. No conversational openings.
4. Provide one line clinical summary

"""


    
response = get_ai_response(msg)

#structured JSON output handling
try:
        if json.loads(response).get("is_critical_emergency"):
                    print(f"Symptoms:{json.loads(response)['detect_symptoms']}")
                    print(f"Clinical reasoning summary:{json.loads(response)['clinical_reasoning_summary']}")
                
                    print(f"- notifying on-call physician")

                    print(f"ALERT: Dispatching emergency SMS to {json.loads(response)['routing_destination']}. "
                        
                        )
        else:
                    print(f"Symptoms:{json.loads(response)['detect_symptoms']}")
                    print(f"Clinical reasoning summary:{json.loads(response)['clinical_reasoning_summary']}")
                    
                    print("System Status: Staging ticket in standard queue.")


        print()
except json.decoder.JSONDecodeError as e:
      
      response = get_ai_response(msg)
      print(response)
      
                