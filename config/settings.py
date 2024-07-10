from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True # production에서는 제거

ALLOWED_HOSTS = ['*']

# CORS 설정
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_CREDENTIALS = True
# CORS_ALLOWED_ORIGINS = [ # 특정 도메인만 허용
#     'http://127.0.0.1:8000',
# ]

# CSRF 설정
# CSRF_TRUSTED_ORIGINS = [
#     'http://localhost:3000',
#     'http://127.0.0.1:8000',
#     "https://port-0-server-1fgm12klx4lo5a1.sel5.cloudtype.app",
# ]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "config.apps.ConfigAppConfig",  # 프로젝트 초기화를 담당하는 앱 등록
    "account",
    "quote",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# djongo는 django ORM을 사용할 수 있지만 성능 및 기능 제한이 있으며 일부 복잡한 쿼리는 지원되지 않는다고 함
# 반면 pymongo는 mongodb에서 mongodb의 공식 python 드라이버이므로 수동적이지만 유연성을 가져 나중에 다른 데에서도 사용 가능
# DATABASES = {
#         'default': {
#             'ENGINE': 'djongo',
#             'NAME': 'your-db-name',
#             'ENFORCE_SCHEMA': False,
#             'CLIENT': {
#                 'host': ''
#             }  
#         }
# }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Django의 기본 메시지와 날짜 형식등이 한국어로 표기
LANGUAGE_CODE = "ko-kr" 
TIME_ZONE = 'Asia/Seoul'

# 다국어 지원
USE_I18N = True
USE_L10N = True
USE_TZ = True

# URL, ROOT 설정
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
