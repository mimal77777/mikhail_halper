from flask import Flask, request
import os
import requests
from chatgpt_handler import ask_chatgpt

app = Flask(__name__)
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
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