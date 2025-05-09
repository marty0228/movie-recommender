import json
import os

# 데이터 파일 경로 설정
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "movies.json")

# 영화 데이터 로딩 함수
def load_movies():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 모든 영화 가져오기
def get_all_movies():
    return load_movies()

# 특정 영화 검색
def get_movie_by_title(title):
    movies = load_movies()
    for movie in movies:
        if movie["title"].lower() == title.lower():
            return movie
    return None

# 특정 장르의 영화 검색
def get_movies_by_genre(genre):
    return [movie for movie in load_movies() if movie["genre"].lower() == genre.lower()]