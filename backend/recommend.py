import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_movies(movie_title, data_path='movies.csv'):
    # 데이터 불러오기
    df = pd.read_csv(data_path)
    
    # 입력된 영화가 데이터셋에 없는 경우 처리
    if movie_title not in df['title'].values:
        print(f"'{movie_title}'은(는) 데이터셋에 없는 영화입니다.")
        return []
    
    # TF-IDF 벡터화
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['description'])
    
    # 유사도 계산
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # 영화 인덱스 찾기
    movie_index_list = df[df['title'] == movie_title].index.tolist()
    if not movie_index_list:
        print(f"'{movie_title}'을(를) 찾을 수 없습니다.")
        return []
    
    movie_index = movie_index_list[0]
    similarity_scores = list(enumerate(cosine_sim[movie_index]))
    
    # 유사도 높은 순으로 정렬
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # 상위 5개 추천 영화 반환 (자기 자신 제외)
    recommendations = [df.iloc[i[0]]['title'] for i in sorted_scores[1:6]]
    return recommendations