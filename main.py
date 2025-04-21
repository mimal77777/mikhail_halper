from flask import Flask, request
import os
import requests
from chatgpt_handler import ask_chatgpt
from pydub import AudioSegment

app = Flask(__name__)
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.json
    message = data["message"]
    chat_id = message["chat"]["id"]

    # Текстовое сообщение
    if "text" in message:
        user_input = message["text"]
        reply = ask_chatgpt(user_input)
        send_message(chat_id, reply)
        return {"ok": True}

    # Голосовое сообщение
    if "voice" in message:
        file_id = message["voice"]["file_id"]
        file_url = get_file_url(file_id)
        ogg_path = "voice.ogg"
        mp3_path = "voice.mp3"

        download_file(file_url, ogg_path)

        audio = AudioSegment.from_ogg(ogg_path)
        audio.export(mp3_path, format="mp3")

        reply = ask_chatgpt(mp3_path, is_audio=True)
        send_message(chat_id, reply)
        return {"ok": True}

    return {"ok": True}

def send_message(chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text}
    )

def get_file_url(file_id):
    file_info = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    ).json()
    file_path = file_info["result"]["file_path"]
    return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

def download_file(url, dest_path):
    response = requests.get(url)
    with open(dest_path, "wb") as f:
        f.write(response.content)

if name == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
