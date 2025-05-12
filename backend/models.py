import json
import os

# ������ ���� ��� ����
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "movies.json")

# ��ȭ ������ �ε� �Լ�
def load_movies():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ��� ��ȭ ��������
def get_all_movies():
    return load_movies()

# Ư�� ��ȭ �˻�
def get_movie_by_title(title):
    movies = load_movies()
    for movie in movies:
        if movie["title"].lower() == title.lower():
            return movie
    return None

# Ư�� �帣�� ��ȭ �˻�
def get_movies_by_genre(genre):
    return [movie for movie in load_movies() if movie["genre"].lower() == genre.lower()]

# ���ο� ��ȭ �߰�
def add_movie(movie):
    movies = load_movies()

    # �ߺ� üũ
    if get_movie_by_title(movie["title"]) is not None:
        return False

    # ���ο� ��ȭ �߰�
    movies.append(movie)

    # ���Ͽ� �ٽ� ����
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

    return True

# ��ȭ ���� �Լ�
def update_movie(title, updated_data):
    movies = load_movies()
    
    # ������ ��ȭ ã��
    for movie in movies:
        if movie["title"].lower() == title.lower():
            movie.update(updated_data)
            
            # ������ �����͸� �ٽ� ���Ͽ� ����
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(movies, f, ensure_ascii=False, indent=4)
            
            return True
    return False

# ��ȭ ���� �Լ� 
def delete_movie(title):
    movies = load_movies()
    updated_movies = [movie for movie in movies if movie["title"].lower() != title.lower()]

    # ������ ��ȭ�� ���� ���
    if len(updated_movies) == len(movies):
        return False

    # ���Ͽ� �ٽ� ����
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_movies, f, ensure_ascii=False, indent=4)

    return True