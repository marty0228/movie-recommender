import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_movies(movie_title, data_path='movies.csv'):
    # ������ �ҷ�����
    df = pd.read_csv(data_path)
    
    # �Էµ� ��ȭ�� �����ͼ¿� ���� ��� ó��
    if movie_title not in df['title'].values:
        print(f"'{movie_title}'��(��) �����ͼ¿� ���� ��ȭ�Դϴ�.")
        return []
    
    # TF-IDF ����ȭ
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['description'])
    
    # ���絵 ���
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # ��ȭ �ε��� ã��
    movie_index_list = df[df['title'] == movie_title].index.tolist()
    if not movie_index_list:
        print(f"'{movie_title}'��(��) ã�� �� �����ϴ�.")
        return []
    
    movie_index = movie_index_list[0]
    similarity_scores = list(enumerate(cosine_sim[movie_index]))
    
    # ���絵 ���� ������ ����
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # ���� 5�� ��õ ��ȭ ��ȯ (�ڱ� �ڽ� ����)
    recommendations = [df.iloc[i[0]]['title'] for i in sorted_scores[1:6]]
    return recommendations