import time
import google.generativeai as genai
import os

# 환경 변수로 API 키 설정 (보안상 더 안전)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Generative AI API 설정
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 텍스트 콘텐츠
content = "나는 사자다. 밀림의 왕이다. 밀린 일이 너무 많다."

# 사용자 프롬프트 생성
user_prompt = f"모든 대답은 한국어로 대답해줘. {content}의 중심 생각의 키워드 하나만 작성해줘"

# 실행 시간 측정
start_time = time.time()

# 콘텐츠 생성 요청
response = model.generate_content(
    user_prompt,
    generation_config=genai.types.GenerationConfig(
        candidate_count=1,
        stop_sequences=['x'],  # 필요시 stop_sequences 수정
        temperature=1.0
    )
)

# 응답 출력
print(response.text)

# 실행 시간 측정 종료
end_time = time.time()
execution_time = end_time - start_time
print(f"실행 시간: {execution_time:.2f} 초")
