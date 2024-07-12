## 업데이트 이력
- [2024-07-10 남기동] 유저 CRUD & 로그인, 명언 CRUD, MongoDB 연결 및 초기화
- [2024-07-12 남기동] ChromaDB 연결, Quote 등록/삭제시 ChromaDB에도 적용, quote_recommend 추가

<br>

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

## Directory Tree
```javascript
project/
├── config/
│   ├── apps.py         # App 시작시 DB 초기화 설정
│   ├── settings.py
│   ├── ...
│   └── urls.py         # URL Mapping
├── account/            # User, Login 관련
│   ├── crud.py         # MongoDB와 상호작용하는 함수
│   ├── serializers.py
│   ├── urls.py         # URL Mapping
│   ├── ...
│   └── views.py        # 웹 요청 처리
├── quote/              # 명언 관련
│   ├── crud.py         # MongoDB와 상호작용하는 함수
│   ├── serializers.py
│   ├── urls.py         # URL Mapping
│   ├── ...
│   └── views.py        # 웹 요청 처리
├── manage.py           # Application Start
├── requirements.txt    # project dependencies
├── .env                # 환경 변수 파일
├── .gitignore        
└── venv/               # 가상 환경
```

<br>

## Model Schema
```python
User {
	_id : ObjectID(자동 생성, PK)
	
	# Not NULL
	email : email
	password : str(~30)
	nickname : str(1~20)
	name : str(~50)
	age : int(1~100)
	sex : Literal['male', 'female']
	birth : str(format:2000-01-01)
	phone : str(format:010-0000-1111)
	
	# NULL --> []로 초기화
	followers : List[user_id] = []
	following : List[user_id] = []
	regiestered_quotes : List[quote_id] = []
	liked_quotes : List[quote_id] = []
}

Quote {
	_id : ObjectID(자동 생성, PK)
	
	# Not NULL
	content: str(~100)
	description : str(~500)   
	author : str              # 해당 명언의 발화자(원저작자)
	registrant : str(user_id) # 등록한 사람(User)
	tag : List[str]
	
	# NULL --> []이나 NULL, 0으로 초기화
	image : ImageField
	likes: int
	comments : List[str] = []
	created_at : datetime
}
```

<br>
