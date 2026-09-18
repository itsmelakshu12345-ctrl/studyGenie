import os
from flask import Flask, render_template, request, jsonify
from google import genai
from chatbot_config import CHATBOT_PROMPT
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.1-flash-lite"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"reply": "Please enter a study question."})

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"{CHATBOT_PROMPT}\n\nStudent question: {message}"
        )
        return jsonify({"reply": response.text})
    except Exception:
        return jsonify({"reply": "Sorry, I could not process your question right now."}), 500

if __name__ == "__main__":
    app.run()
