from flask import Flask, jsonify, request, render_template, redirect, url_for
from models import get_all_movies, get_movie_by_title, get_movies_by_genre,add_movie,update_movie, delete_movie
from recommend import recommend_movies

app = Flask(__name__)

# 기본 JSON 인코딩 설정 (한글 깨짐 방지)
app.config['JSON_AS_ASCII'] = False

# 기본 홈 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 모든 영화 목록 조회 (API)
@app.route('/api/movies', methods=['GET'])
def get_movies():
    return jsonify(get_all_movies())

# 영화 추가 (API)
@app.route('/api/movies', methods=['POST'])
def add_movie_api():
    new_movie = request.json
    if add_movie(new_movie):
        return jsonify({"message": "영화가 성공적으로 추가되었습니다."}), 201
    else:
        return jsonify({"error": "이미 존재하는 영화입니다."}), 409

# 영화 검색, 수정, 삭제 (API)
@app.route('/api/movies/<title>', methods=['GET', 'PUT', 'DELETE'])
def manage_movie_api(title):
    # 영화 조회
    if request.method == 'GET':
        movie = get_movie_by_title(title)
        if movie:
            return jsonify(movie)
        else:
            return jsonify({"error": f"'{title}' 영화를 찾을 수 없습니다."}), 404
    
    # 영화 수정
    if request.method == 'PUT':
        updated_data = request.json
        if update_movie(title, updated_data):
            return jsonify({"message": f"'{title}' 영화가 성공적으로 수정되었습니다."}), 200
        else:
            return jsonify({"error": f"'{title}' 영화를 찾을 수 없습니다."}), 404
    
    # 영화 삭제
    if request.method == 'DELETE':
        if delete_movie(title):
            return jsonify({"message": f"'{title}' 영화가 성공적으로 삭제되었습니다."}), 200
        else:
            return jsonify({"error": f"'{title}' 영화를 찾을 수 없습니다."}), 404

# 영화 추가 폼 (HTML)
@app.route('/movies/add', methods=['GET', 'POST'])
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
            return redirect(url_for('home'))
        else:
            return "이미 존재하는 영화입니다.", 409
    
    return render_template('add_movie.html')

# 영화 수정 폼 (HTML)
@app.route('/movies/edit/<title>', methods=['GET', 'POST'])
def edit_movie_form(title):
    movie = get_movie_by_title(title)
    
    # 영화가 없으면 404 에러 반환
    if not movie:
        return jsonify({"error": f"'{title}' 영화를 찾을 수 없습니다."}), 404

    if request.method == 'POST':
        # 폼에서 전달된 수정된 영화 데이터 가져오기
        updated_data = {
            "title": request.form['title'],
            "genre": request.form['genre'],
            "rating": float(request.form['rating']),
            "year": int(request.form['year'])
        }

        # 영화 수정
        if update_movie(title, updated_data):
            return redirect(url_for('home'))
        else:
            return "수정에 실패했습니다.", 500

    return render_template('edit_movie.html', movie=movie)



@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form.get('movie_title')
    recommendations = recommend_movies(movie_title, data_path='movies.csv')
    return render_template('index.html', movie_title=movie_title, recommendations=recommendations)


if __name__ == '__main__':
    app.run(port=5000, debug=True)