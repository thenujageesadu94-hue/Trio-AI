import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# 🚨 මෙතන Token එක කෙලින්ම ලියන්නේ නැහැ. 
# අපි Render එකේ 'Environment Variables' වලට GITHUB_TOKEN කියලා මේක දානවා.
token = os.environ.get("GITHUB_TOKEN")

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=token,
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question")
    
    # AI Logic (Sinhala/Native Script rules)
    system_prompt = """Your name is Trio AI. 
    1. If user asks in Sinhala/Singlish, answer in Sinhala Script (සිංහල අකුරෙන්).
    2. If user writes other languages in English letters (Kaise ho), answer in their Native Script.
    3. Be friendly like a Sri Lankan friend (machan, macho).
    4. Use Markdown for formatting."""

    try:
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
        return jsonify({"answer": "⚠️ Connection error. Please check API settings."})

if __name__ == "__main__":
    # වෙබ් එකේ දානකොට Port එක auto සෙට් වෙනවා
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)