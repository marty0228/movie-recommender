from flask import Flask, jsonify, request, render_template, redirect, url_for
from models import get_all_movies, get_movie_by_title, get_movies_by_genre,add_movie

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

@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'GET':
        return jsonify(get_all_movies())
    
    if request.method == 'POST':
        new_movie = request.json
        if add_movie(new_movie):
            return jsonify({"message": "영화가 성공적으로 추가되었습니다."}), 201
        else:
            return jsonify({"error": "이미 존재하는 영화입니다."}), 409
        
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

# 새로운 영화 추가 폼
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie_form():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        rating = float(request.form['rating'])
        year = int(request.form['year'])
        
        new_movie = {
            "title": title,
            "genre": genre,
            "rating": rating,
            "year": year
        }

        if add_movie(new_movie):
            return redirect(url_for('add_movie_form'))
        else:
            return "이미 존재하는 영화입니다.", 409
    
    return render_template('add_movie.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)