import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Render 설정창에 넣은 'GEMINI_API_KEY'를 불러오는 거야 ㅋ
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 모델 리스트 다 훑지 말고 그냥 바로 선언해 ㅋ
def get_model():
    try:
        # gemini-1.5-flash-latest가 제일 가볍고 빠름
        return genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest', 
            system_instruction="너의 이름은 'AI'다. 대답은 무조건 한국어로만, 자세하고 존댓말, 화내지마. 주인은 이세미다."
        )
    except:
        return None

model = get_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    if not model:
        return jsonify({'response': '서버 설정 확인해주세요.'})
    
    user_msg = request.json.get('message')
    try:
        response = model.generate_content(user_msg)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': '에러가 났습니다.'})

if __name__ == '__main__':
    # 배포용 포트 설정 (Render는 알아서 잡지만 일단 이렇게 써 ㅋ)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


