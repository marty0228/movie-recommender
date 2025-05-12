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

# 새로운 영화 추가
def add_movie(movie):
    movies = load_movies()

    # 중복 체크
    if get_movie_by_title(movie["title"]) is not None:
        return False

    # 새로운 영화 추가
    movies.append(movie)

    # 파일에 다시 저장
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

    return True

# 영화 수정 함수
def update_movie(title, updated_data):
    movies = load_movies()
    
    # 수정할 영화 찾기
    for movie in movies:
        if movie["title"].lower() == title.lower():
            movie.update(updated_data)
            
            # 수정된 데이터를 다시 파일에 저장
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(movies, f, ensure_ascii=False, indent=4)
            
            return True
    return False

# 영화 삭제 함수 
def delete_movie(title):
    movies = load_movies()
    updated_movies = [movie for movie in movies if movie["title"].lower() != title.lower()]

    # 삭제할 영화가 없는 경우
    if len(updated_movies) == len(movies):
        return False

    # 파일에 다시 저장
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_movies, f, ensure_ascii=False, indent=4)

    return True