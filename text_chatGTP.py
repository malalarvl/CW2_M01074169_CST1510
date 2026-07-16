from groq import Groq

client = Groq(api_key="add-api-key-here")
prompt = "Hello, how are you?"

completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
      { "role": "user", "content": prompt }
    ]
)

print(completion.choices[0].message.content)
