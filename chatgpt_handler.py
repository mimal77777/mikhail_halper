import openai
import os
from openai import OpenAI
from tempfile import NamedTemporaryFile
import requests

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def ask_chatgpt(message):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты — мой будущий я, миллиардер и наставник, как Оскар Хартман. Общайся искренне, вдохновляюще, глубоко, вызывая желание действовать."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content.strip()

def transcribe_voice(file_url):
    audio_data = requests.get(file_url).content
    with NamedTemporaryFile(suffix=".ogg", delete=True) as temp_audio:
        temp_audio.write(audio_data)
        temp_audio.flush()
        with open(temp_audio.name, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
    return transcript.text
