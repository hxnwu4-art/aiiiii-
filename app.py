import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Render 설정창에 넣은 'GEMINI_API_KEY'를 불러오는 거야 ㅋ
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return genai.GenerativeModel(
                model_name=m.name,
                system_instruction="너의 이름은 '에이아이'다. 무조건 한국어로만, 모든걸 자세하게, 친절하게, 존댓말 사용해서 해줘. 화내면 안돼. 주인 이름은 이세미다."
            )
    return None

model = get_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    if not model:
        return jsonify({'response': '서버 설정 확인해 ㅋ'})
    
    user_msg = request.json.get('message')
    try:
        response = model.generate_content(user_msg)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': '에러남 ㅋ'})

if __name__ == '__main__':
    # 배포용 포트 설정 (Render는 알아서 잡지만 일단 이렇게 써 ㅋ)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
