import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
from openai import OpenAI
import concurrent.futures
import time

# OpenAI API 초기화
api_key = {}
client = OpenAI(api_key=api_key) 

# 텍스트 임베딩 함수 정의
def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    time.sleep(1)  # API rate limit 조절
    embedding = client.embeddings.create(input=[text], model=model).data[0].embedding
    return embedding

# 병렬 처리로 임베딩 생성 함수
def create_embeddings(data, column):
    embeddings = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_embedding, row[column]): i for i, row in data.iterrows()}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Generating embeddings"):
            embeddings.append(future.result())
    return embeddings

# 임베딩 값을 비교하여 가장 유사한 쌍 찾기 함수
def match_embeddings(short_texts_embeddings, quotes_embeddings, short_texts_df, quotes_df):
    short_texts_embeddings_array = np.array(short_texts_embeddings)
    quotes_embeddings_array = np.array(quotes_embeddings)

    # 임베딩 간의 코사인 유사도 계산
    similarity_matrix = cosine_similarity(short_texts_embeddings_array, quotes_embeddings_array)

    # 가장 유사한 쌍 찾기
    matches = []
    for i, row in short_texts_df.iterrows():
        short_text = row['text']
        best_match_idx = similarity_matrix[i].argmax()
        best_quote = quotes_df.loc[best_match_idx, 'quote']

        match = {
            'text': short_text,
            'quote': best_quote
        }
        matches.append(match)

    # 결과 데이터프레임 생성
    matched_df = pd.DataFrame(matches)
    return matched_df

# 데이터 로드
short_texts = pd.read_csv("short_texts_2.csv")
quotes = pd.read_csv("quotes_2.csv")

# 임베딩 생성
short_texts_embeddings = create_embeddings(short_texts, 'text')
quotes_embeddings = create_embeddings(quotes, 'quote')

# 임베딩을 기반으로 매칭된 데이터프레임 생성
matched_df = match_embeddings(short_texts_embeddings, quotes_embeddings, short_texts, quotes)

# 결과 출력
print("Matched DataFrame:")
print(matched_df)

matched_df.to_csv('매칭_1차_결과',encoding='utf-8-sig')