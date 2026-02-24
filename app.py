from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# 키 확인해라 ㅋ
genai.configure(api_key="AIzaSyAb7XZ0a_KUkBuNdmacA_7v_7jx6nuuc2g")

def get_model():
    # 니 컴퓨터에서 사용 가능한 모델을 직접 찾아서 설정함
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"찾았다 요놈: {m.name}")
            # 여기서 네가 원하는 자아를 주입하는 거임 ㅋ
            return genai.GenerativeModel(
                model_name=m.name,
                system_instruction="너의 이름은 'ㅗ'다. 무조건 한국어로만 짧고 띠껍고 나쁜 말투로 대답해. 뭐만하면 욕써(시발년아, 시발, 개새끼야 등등..). 주인 이름은 전현우다."
            )
    return None

model = get_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    if not model:
        return jsonify({'response': '모델이 안 잡힌다니까? 키 확인해 ㅋ'})
    
    user_msg = request.json.get('message')
    try:
        # 아까처럼 단순 text만 오는 게 아니라 세뇌된 자아로 대답함
        response = model.generate_content(user_msg)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f'에러 또 났네 ㅋ: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
