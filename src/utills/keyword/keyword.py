import sys
import requests
import json

CLINET_ID = "afqcfylarl"
CLINET_SECRET = "D9bFrNKjZS0iIPlGrfBi4QqHmztX8oQCtf0Hugey"
URL = 'https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize'

headers = {
    'Accept': 'application/json;UTF-8', 
    'Content-Type': 'application/json;UTF-8', 
    'X-NCP-APIGW-API-KEY-ID': CLINET_ID, 
    'X-NCP-APIGW-API-KEY': CLINET_SECRET
}

def get_completion(text):
    data = {
        "document": {"content": text}, 
        "option": {
            "language": "ko", 
            "model": "news", 
            "tone": 2, 
            "summaryCount": 3
        }
    }

    response = requests.post(URL, headers=headers, data=json.dumps(data).encode('UTF-8'))
    rescode = response.status_code
    if rescode == 200:
        print(response.text)
    else:
        print("Error : " + response.text)

def get_keyword(search_query):
    text = f"{search_query} 이 감정의 무드의 단어를 한개 만들어줘."
    get_completion(text)

if __name__ == '__main__':
    search_query = input("키워드를 입력하세요: ")
    get_keyword(search_query)
