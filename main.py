from flask import Flask, request
import os
import requests
from chatgpt_handler import ask_chatgpt, transcribe_voice

app = Flask(__name__)
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]

    if "voice" in data["message"]:
        file_id = data["message"]["voice"]["file_id"]
        file_info = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        ).json()
        file_path = file_info["result"]["file_path"]
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        message = transcribe_voice(file_url)
    else:
        message = data["message"].get("text", "")

    if not message:
        return {"ok": True}

    reply = ask_chatgpt(message)

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )

    return {"ok": True}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
