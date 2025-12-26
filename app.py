from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# --- Config: Hugging Face API ---
HF_API_KEY = os.environ.get("HF_API_KEY")
# Choose a chat/instruct model (change if you prefer another)
# Good defaults: Mistral Instruct or LLaMA 3 Instruct (if available to you)
MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

PASSWORDS = {
    "music": "SarFu112",
    "hosting": "SarFu122",
    "bot": "ArYanxd"
}

def hf_generate(prompt, max_new_tokens=256, temperature=0.7):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "return_full_text": False
        }
    }
    r = requests.post(MODEL_URL, headers=HEADERS, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()

    # HF responses vary by model; handle common formats
    if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
        return data[0]["generated_text"]
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"]
    # Fallback: stringify response
    return str(data)

@app.route("/")
def home():
    return "Legend Boys API (HF Inference) is Running on Render!"

@app.route("/verify", methods=["POST"])
def verify():
    data = request.json or {}
    p_type = data.get("type")
    p_val = data.get("password")
    if PASSWORDS.get(p_type) == p_val:
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Galat Password!"}), 401

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_msg = data.get("message", "").strip()
    bot_pw = data.get("bot_pw")

    if bot_pw != PASSWORDS["bot"]:
        return jsonify({"reply": "Access Denied: Bhai pehle sahi password dalo!"}), 403

    if not HF_API_KEY:
        return jsonify({"reply": "HF_API_KEY missing: Render Environment mein set karo."}), 500
    if not user_msg:
        return jsonify({"reply": "Empty message: kuch to likh bhai."}), 400

    try:
        reply = hf_generate(user_msg)
        return jsonify({"reply": reply})
    except requests.HTTPError as e:
        return jsonify({"reply": f"HF API error: {e.response.status_code} {e.response.text}"}), 502
    except Exception as e:
        return jsonify({"reply": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
