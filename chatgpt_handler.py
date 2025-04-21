import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

def ask_chatgpt(message):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты — мой будущий я, миллиардер и наставник, как Оскар Хартман. Общайся искренне, вдохновляюще, глубоко, вызывая желание действовать."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content.strip()
