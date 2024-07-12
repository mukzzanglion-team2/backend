import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from database.chroma_manager import ChromaManager

# .env 파일을 현재 작업 디렉토리에서 로드
load_dotenv() 

# Mongo DB
CONNECTION_STRING = os.getenv("CONNECTION_STRING")  

# Chroma DB
CHROMA_HOST = os.environ.get("CHROMA_HOST")
CHROMA_PORT = os.environ.get("CHROMA_PORT")

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
            print("MongoDB Connection Succeed")
            return client
        except ConnectionFailure:
            print("Failed to connect to MongoDB")
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
        print("Try to reconnect MongoDB")
        MongoClientSingleton.reconnect()
        client = MongoClientSingleton.get_client()
    return client

class ChromaManagerSingleton(ChromaManager):
    _manager = None

    @classmethod
    def get_client(cls):
        if cls._manager is None:
            cls._manager = cls._connect()
        return cls._manager

    @classmethod
    def _connect(cls):
        try:
            manager = ChromaManager(host=CHROMA_HOST, port=CHROMA_PORT)
            print("ChromaDB Connection Succeed")
            return manager
        except ConnectionFailure:
            print("Failed to connect to ChromaDB")
            return None

    @classmethod
    def reconnect(cls):
        cls._manager = cls._connect()

def vector_connect(): 
    manager = ChromaManagerSingleton.get_client()
    # 연결 상태 확인 및 재연결
    try:
        if manager is not None:
            print("ChromaDB is active!\n")
    except ConnectionFailure:
        print("Try to reconnect ChromaDB\n")
        ChromaManagerSingleton.reconnect()
        manager = ChromaManagerSingleton.get_client()
    return manager