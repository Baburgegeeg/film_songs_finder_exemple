import os
from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

# 1. Проверяем переменную окружения (для хостинга Render)
api_key = os.environ.get("GROQ_API_KEY")

# 2. Если запускаем локально в VS Code, используем твой новый ключ
if not api_key:
    api_key = "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"

# Инициализируем клиента Groq
client = Groq(api_key=api_key)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        user_request = request.form.get('user_request')
        
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert in movie soundtracks and music. The user will describe "
                            "a movie and a scene. Your task is to identify the most likely songs playing "
                            "in that scene. "
                            "CRITICAL INSTRUCTIONS:\n"
                            "1. Respond strictly in English.\n"
                            "2. For every song you suggest, you MUST provide a clickable HTML hyperlink to YouTube search. "
                            "Use this exact format for links: <a href=\"https://www.youtube.com/results?search_query=Song+Name+Artist+Name\" target=\"_blank\">Listen on YouTube 🎥</a>\n"
                            "3. Replace 'Song+Name+Artist+Name' in the URL with the actual song title and artist, using plus signs (+) instead of spaces.\n"
                            "4. Keep your response concise, polite, and well-formatted."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_request,
                    }
                ],
                model="llama-3.1-8b-instant",
            )
            
            result = chat_completion.choices[0].message.content
            
        except Exception as e:
            result = f"An error occurred while connecting to the AI: {e}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    # Настройка портов для корректной работы и на ПК, и на Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
