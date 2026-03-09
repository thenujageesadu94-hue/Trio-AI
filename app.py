import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# 🔒 මෙන්න උඹේ Token එක මම කෙලින්ම කෝඩ් එකට දැම්මා.
# (පස්සේ කාලෙක මේක Environment Variables වලට දාගන්න එක හොඳයි මචං)
token = "ghp_Y1nS9tU2mE6rZ4xQ8vP0aW7bC3dX5fG6hI9j" 

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=token,
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_input = data.get("question")
        
        system_prompt = """Your name is Trio AI. 
        1. If user asks in Sinhala/Singlish, answer in Sinhala Script (සිංහල අකුරෙන්).
        2. If user writes other languages in English letters, answer in their Native Script.
        3. Be friendly like a Sri Lankan friend (machan, macho).
        4. Use Markdown for formatting."""

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            model="gpt-4o-mini",
            temperature=0.85
        )
        return jsonify({"answer": response.choices[0].message.content})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"answer": "⚠️ Connection error. API එකේ පොඩි අවුලක් තියෙනවා."})

if __name__ == "__main__":
    app.run(debug=True)
