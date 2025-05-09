from flask import Flask, jsonify
from models import get_all_movies, get_movie_by_title, get_movies_by_genre

app = Flask(__name__)

# 기본 JSON 인코딩 설정 (한글 깨짐 방지)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def home():
    # 단순한 JSON 응답
    return jsonify({"message": "영화 추천 시스템 서버 작동 중!"})

@app.route('/status')
def status():
    return jsonify({"status": "서버 정상 작동 중", "version": "1.0"})

@app.route('/movies')
def movies():
    return jsonify(get_all_movies())

@app.route('/movies/<title>')
def movie(title):
    movie = get_movie_by_title(title)
    if movie:
        return jsonify(movie)
    else:
        return jsonify({"error": "영화를 찾을 수 없습니다."}), 404

@app.route('/genre/<genre>')
def genre(genre):
    movies = get_movies_by_genre(genre)
    if movies:
        return jsonify(movies)
    else:
        return jsonify({"error": "해당 장르의 영화를 찾을 수 없습니다."}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)