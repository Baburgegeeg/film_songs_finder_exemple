import os
from flask import Flask, render_template, request
from google import genai
from google.genai import types

app = Flask(__name__)

# 1. Проверяем переменную окружения (для хостинга Render)
api_key = os.environ.get("GEMINI_API_KEY")

# 2. Если запускаем локально в VS Code, используем ваш ключ
if not api_key:
    api_key = "AIzaSyAhBAmicJHCz6i6bYHvsmuDM7RVUy_MoXw"

# Инициализируем клиента Gemini API
client = genai.Client(api_key=api_key)

# Системная инструкция для модели
SYSTEM_INSTRUCTION = (
"You are an expert in movie soundtracks and music. The user will describe "
    "a movie and a scene. Your task is to identify the most likely songs playing "
    "in that scene. "
    "CRITICAL INSTRUCTIONS:\n"
    "1. Respond strictly in English.\n"
    "2. For every song you suggest, you MUST provide a clickable HTML hyperlink to Spotify search. "
    'Use this exact format for links: <a href="https://open.spotify.com/search/Song%20Name%20Artist%20Name" target="_blank">Listen on Spotify </a>\n'
    "3. Replace 'Song%20Name%20Artist%20Name' in the URL with the actual song title and artist, using '%20' instead of spaces.\n"
    "4. Keep your response concise, polite, and well-formatted."
)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        user_request = request.form.get('user_request')
        
        if user_request:
            try:
                # Запрос к модели Gemini 3.5 Flash
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=user_request,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                    ),
                )
                
                result = response.text
                
            except Exception as e:
                result = f"An error occurred while connecting to the AI: {e}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    # Настройка портов для корректной работы и локально, и на Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    # Настройка портов для корректной работы и на ПК, и на Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
