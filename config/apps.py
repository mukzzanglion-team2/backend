from django.apps import AppConfig
from database import db_connect

class ConfigAppConfig(AppConfig):
    name = 'config'

    def ready(self):
        print("Initializing....")
        # MongoDB 클라이언트 초기화
        db_connect()