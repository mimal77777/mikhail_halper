import os
from openai import OpenAI

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def ask_chatgpt(message):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты — мой будущий я, миллиардер и наставник, как Оскар Хартман. Общайся искренне, вдохновляюще, глубоко, вызывая желание действовать."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content.strip()
