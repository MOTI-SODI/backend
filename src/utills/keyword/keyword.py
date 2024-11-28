from dotenv import load_dotenv
import requests
import openai
import json
import os

load_dotenv(dotenv_path="./config/.env")

GPT_KEY = os.environ.get('GPT_KEY')

openai.api_key = GPT_KEY

def get_completion(prompt):
    message = [
        {"role": "system", "content": "사용자의 입력에서 중심적인 테마와 개념을 추출하여 추상적인 아이디어나 감정을 전달하는 키워드나 문구로 반환하세요."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=1,
    )
    return response.choices[0].message["content"]
