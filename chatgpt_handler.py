import openai
import os
import requests
import tempfile

openai.api_key = os.environ.get("OPENAI_API_KEY")

def ask_chatgpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты — мой будущий я, миллиардер и наставник, как Оскар Хартман. Общайся искренне, вдохновляюще, глубоко, вызывая желание действовать."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content.strip()


def transcribe_voice(file_url):
    audio_data = requests.get(file_url).content
    with tempfile.NamedTemporaryFile(delete=False, suffix=".oga") as temp_audio:
        temp_audio.write(audio_data)
        temp_audio.flush()

        with open(temp_audio.name, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)

    return transcript["text"]
