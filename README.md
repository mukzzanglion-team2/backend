## 설치방법
```
git clone https://github.com/mukzzanglion-team2/backend.git
cd backend
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

<br>

## 참고할 노션 페이지
https://www.notion.so/rmdnps10/Back-End-60d517d1690b44bc9d4c0ded0b839ec9

<br>

## .env 파일
```
SECRET_KEY = "django-insecure-_38220%fxx8=0fyc+!4g0fljnljvvw2l0w92v_sz_vx_3n3qh-"
CONNECTION_STRING = "mongodb+srv://admin:admin@cluster0.ky8ocah.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
OPENAI_API_KEY = "sk-proj-Oks7bA2Pt1lQqXrWoEXbT3BlbkFJrb2rZomXU0hBQBaWnKtM"
CHROMA_HOST = "20.249.169.164"
CHROMA_PORT = "8001"
```

<br>

## 업데이트 이력
- [2024-07-10 남기동] 유저 CRUD & 로그인, 명언 CRUD, MongoDB 연결 및 초기화
- [2024-07-12 남기동] ChromaDB 연결, Quote 등록/삭제시 ChromaDB에도 적용, quote_recommend 추가
