from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client=OpenAI()
r=client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0,
    messages=[
        {"role": "user", "content": "Reply with exactly one word: sports"}
    ]
)
print(r.choices[0].message.content)
print(r.usage)