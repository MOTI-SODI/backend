import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="./config/.env")
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

def generate_keyword(content):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    user_prompt = f"모든 대답은 한국어로 대답해줘. {content}의 중심 생각의 키워드 하나만 작성해줘"

    response = model.generate_content(
        user_prompt,
        generation_config=genai.types.GenerationConfig(
            candidate_count=1,
            stop_sequences=['x'],
            temperature=1.0
        )
    )

    response_text = response.text.replace("\n", "").strip()
    return response_text
