import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

def ask_chatgpt(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=1000,
        temperature=0.8
    )
    return response["choices"][0]["text"].strip()
