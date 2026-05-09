import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if GEMINI_API_KEY and GEMINI_API_KEY != 'your_gemini_api_key_here':
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = None

def get_chatbot_response(prompt):
    if not client:
        return 'AI configuration missing. Please set GEMINI_API_KEY in .env.'
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return str(e)

def generate_explanation(detected_objects):
    if not client:
        return 'Explanation generation unavailable.', 'UNKNOWN'
    prompt = f'Analyze this detection result for a night surveillance system: {detected_objects}. Provide a brief intelligent explanation and assess the risk level (LOW, MEDIUM, HIGH).'
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        text = response.text
        risk_level = 'LOW'
        if 'HIGH' in text.upper(): risk_level = 'HIGH'
        elif 'MEDIUM' in text.upper(): risk_level = 'MEDIUM'
        return text, risk_level
    except Exception as e:
        return f'Error generating explanation: {e}', 'UNKNOWN'