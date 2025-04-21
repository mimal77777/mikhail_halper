from flask import Flask, request
import os
import requests
from chatgpt_handler import ask_chatgpt

app = Flask(__name__)
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    message = data["message"].get("text", "")
    
    # === Обработка голосового сообщения ===
    voice = data["message"].get("voice")
    if voice:
        file_id = voice["file_id"]
        file_info = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
        file_path = file_info["result"]["file_path"]
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        # Сохраняем и конвертируем голосовое
        ogg_path = "voice.ogg"
        wav_path = "voice.wav"
        with open(ogg_path, "wb") as f:
            f.write(requests.get(file_url).content)
        os.system(f"ffmpeg -i {ogg_path} {wav_path}")

        # Расшифровка аудио через Whisper
        import openai
        openai.api_key = OPENAI_API_KEY
        with open(wav_path, "rb") as audio:
            transcript = openai.Audio.transcribe("whisper-1", audio)
            message = transcript["text"]

    if not message:
        return {"ok": True}

    reply = ask_chatgpt(message)

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )
    return {"ok": True}

if name == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
