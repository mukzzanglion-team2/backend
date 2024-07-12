import os
from dotenv import load_dotenv
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.schema import Document

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
QUOTE_COLLECTION = 'Quote'

class ChromaManager():
    def __init__(self, host:str, port:str) -> None:
        self.connected = False
        self.embedding_function = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
        self.__connect_db__(host, port)
    
    def __connect_db__(self, host, port):
        try:
            self.client = chromadb.HttpClient(host=host, port=port) # DB 접속 시도
            print(f'chromadb [version : {self.client.get_version()}] connected.')
            self.connected = True
        except Exception as e:
            print(e)
            return
        
        # get collection
        self.quotes = self.__get_collection__(QUOTE_COLLECTION)
        self.quote_db = Chroma(
            client = self.client,
            collection_name = QUOTE_COLLECTION,
            embedding_function = self.embedding_function
        )

    def __get_collection__(self, name:str):
        if any(collection.name == name for collection in self.client.list_collections()):
            print(f'{name}Collection Found\n')
            return self.client.get_collection(name)
        else:
            print(f"{name} Collection Not Found. Creating the Collection\n")
            try:
                collection = self.client.create_collection(
                    name=name,
                    metadata={"hnsw:space": "cosine"},
                    embedding_function=self.embedding_function, # 미리 설정해두면 embed_query를 안해줘도 similarity_search에 str형태의 query만 넘겨주면 해당 embedding 모델로 embedding해서 검색에 사용 
                )
                print("Collection created:", collection)
                return collection
            except KeyError as e:
                print(f"KeyError: {e}")
                raise

    def add_quote(self, description:str, quote_id:str, quote:str, author:str):
        try:
            doc = Document(
                page_content=description, # quote의 description 기반으로 검색하고
                metadata={
                    'quote_id' : quote_id,# quote의 고유 ID(PK)
                    'quote': quote,       # quote의 content 확인용
                    'author' : author,    # quote의 원저작자 확인용
                }
            )
            # print("Document to be added:", doc)
            result = self.quote_db.add_documents([doc])
            return result
        except Exception as e:
            print(f"Error in add_quote : {e}")
            raise
        
    def delete_quote_by_quote_id(self, quote_id:str):
        self.quotes.delete(where={'quote_id': quote_id})
        
    def get_quote_by_quote_id(self, quote_id:str):
        return self.quotes.get(where={'quote_id': quote_id})

    def search_quote(self, query:str):
        retrieved_quote = self.quote_db.similarity_search(
            query=query, k = 1
        )
        return retrieved_quote # List[Document]