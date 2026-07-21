import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

print("API Loaded:", api_key[:10] + "...")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "Hello"
        }
    ],
    temperature=0.7,
    max_tokens=100
)

print("\nAI Response:\n")
print(response.choices[0].message.content)