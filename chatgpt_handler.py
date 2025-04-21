import openai
import os

api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def ask_chatgpt(message, is_audio=False):
    if is_audio:
        # message — путь к mp3-файлу
        with open(message, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        message = transcript.text

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты — мой будущий я, миллиардер и наставник, как Оскар Хартман. Общайся искренне, вдохновляюще, глубоко."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content.strip()
