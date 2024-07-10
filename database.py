import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# .env 파일을 현재 작업 디렉토리에서 로드
load_dotenv() 

# # Chroma DB
# HOST = os.getenv("VECTOR_HOST")
# PORT = os.getenv("VECTOR_PORT")

# Mongo DB
CONNECTION_STRING = os.getenv("CONNECTION_STRING")  

class MongoClientSingleton:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = cls._connect()
        return cls._client

    @classmethod
    def _connect(cls):
        try:
            client = MongoClient(CONNECTION_STRING)
            # 연결 테스트
            client.admin.command('ping')
            print("Connection Succeed\n")
            return client
        except ConnectionFailure:
            print("Failed to connect to MongoDB\n")
            return None

    @classmethod
    def reconnect(cls):
        cls._client = cls._connect()

def db_connect(): 
    client = MongoClientSingleton.get_client()
    # 연결 상태 확인 및 재연결
    try:
        if client is not None:
            client.admin.command('ping')
    except ConnectionFailure:
        print("Try to reconnect\n")
        MongoClientSingleton.reconnect()
        client = MongoClientSingleton.get_client()
    return client
