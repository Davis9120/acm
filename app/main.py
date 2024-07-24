# app/main.py
import openai
import os

# OpenAI APIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    print("ChatGPT Response:", generate_response(user_prompt))
