import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_comment(name, avg_score):
    prompt = f"Write a one-sentence teacher's comment for a student named {name} who scored an average of {avg_score:.1f}%."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=50
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"No comment available due to error: {e}"
