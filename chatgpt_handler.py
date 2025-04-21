import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

def ask_chatgpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Ты — мой будущий я, миллиардер и наставник, как Оскар Хартманн. Общайся искренне, вдохновляюще, глубоко, вызывая желание действовать."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )
    return response['choices'][0]['message']['content'].strip()
