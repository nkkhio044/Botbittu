from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# --- Configure Gemini API Key from Render Environment ---
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# --- Initialize Gemini Model ---
# Use a valid model name (latest supported ones are gemini-1.5-flash-latest or gemini-2.0-flash)
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

# --- Passwords for Access Control ---
PASSWORDS = {
    "music": "SarFu112",     # Avii Raj ke button ka password
    "hosting": "SarFu122",   # Nawab ke button ka password
    "bot": "ArYanxd"         # Chat Bot kholne ka password
}

# --- Home Route ---
@app.route('/')
def home():
    return "Legend Boys API is Running on Render!"

# --- Password Verification Route ---
@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    p_type = data.get("type")
    p_val = data.get("password")

    if PASSWORDS.get(p_type) == p_val:
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Galat Password!"})

# --- Gemini Chatbot Route ---
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get("message")
    bot_pw = data.get("bot_pw")

    if bot_pw != PASSWORDS["bot"]:
        return jsonify({"reply": "Access Denied: Bhai pehle sahi password dalo!"})

    try:
        response = model.generate_content(user_msg)
        reply_text = response.text if hasattr(response, "text") else response.candidates[0].content.parts[0].text
        return jsonify({"reply": reply_text})
    except Exception as e:
        print("Gemini Error:", e)
        return jsonify({"reply": f"Bhai error aa gaya: {str(e)}"})

# --- Run App on Render Default Port ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT automatically
    app.run(host='0.0.0.0', port=port)
