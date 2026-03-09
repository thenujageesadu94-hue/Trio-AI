import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# ඔයාගේ GitHub Token එක මෙතන තියෙනවා
TOKEN = "ghp_m0Vn0EbeGj1m3o9oF86V6850M0M0N0E0"

# OpenAI Client එක හරියටම Setup කිරීම
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=TOKEN
)

@app.route("/")
def index():
    # Templates ෆෝල්ඩර් එක ඇතුළේ index.html තියෙන්නම ඕනේ
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"answer": "ප්‍රශ්නයක් ලැබුණේ නැහැ මචං!"})

        user_input = data.get("question")
        
        # AI එකෙන් Response එක ලබා ගැනීම
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Your name is Trio AI. Be a friendly Sri Lankan friend. Answer in Sinhala script for Sinhala/Singlish questions."},
                {"role": "user", "content": user_input}
            ],
            model="gpt-4o-mini"
        )
        return jsonify({"answer": response.choices[0].message.content})
    except Exception as e:
        # මොකක් හරි Error එකක් වුණොත් ඒක මෙතනින් බලාගන්න පුළුවන්
        return jsonify({"answer": f"⚠️ Connection error: {str(e)}"})

if __name__ == "__main__":
    app.run()
