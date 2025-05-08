from flask import Flask, jsonify

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

if __name__ == '__main__':
    app.run(port=5000, debug=True)