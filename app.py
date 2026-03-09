import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# මෙන්න උඹේ අලුත් Token එක (පරිස්සමෙන් පාවිච්චි කරපන්)
TOKEN = "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"

# OpenAI Client එක Setup කිරීම
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=TOKEN
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"answer": "ප්‍රශ්නයක් ලැබුණේ නැහැ මචං!"})

        user_input = data.get("question")
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Your name is Trio AI. Be a friendly Sri Lankan friend. Answer in Sinhala script for Sinhala/Singlish questions."},
                {"role": "user", "content": user_input}
            ],
            model="gpt-4o-mini"
        )
        return jsonify({"answer": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"answer": f"⚠️ Connection error: {str(e)}"})

if __name__ == "__main__":
    app.run()
