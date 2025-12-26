from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# API Configuration
# Bhai maine teri key wahi rehne di hai
genai.configure(api_key="AIzaSyAUq4F8mf1FLQyZhV3T6Fp8AGe-DwQ0e_U")

# Fixed: Latest model name (Gemini 1.5 Flash)
# Ye model fast bhi hai aur free tier mein best chalta hai
model = genai.GenerativeModel('gemini-1.5-flash')

# Secret Passwords
PASSWORDS = {
    "music": "SarFu112",
    "hosting": "SarFu122",
    "bot": "ArYanxd"
}

@app.route('/')
def home():
    return "Legend Boys API is Running Successfully!"

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    p_type = data.get("type")
    p_val = data.get("password")
    
    if PASSWORDS.get(p_type) == p_val:
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Galat Password!"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get("message")
    bot_pw = data.get("bot_pw")

    if bot_pw != PASSWORDS["bot"]:
        return jsonify({"reply": "Access Denied: Bhai pehle sahi password dalo!"})

    try:
        # Seedha generation use kar rahe hain jo latest API ke liye sahi hai
        response = model.generate_content(user_msg)
        
        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "Bhai, Google ne reply empty bheja hai. Fir se try karo."})
            
    except Exception as e:
        return jsonify({"reply": f"Bhai error aa gaya: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
