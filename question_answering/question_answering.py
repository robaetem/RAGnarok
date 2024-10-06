from openai import OpenAI
import os
from dotenv import load_dotenv

def get_openai_client():
    load_dotenv()
    OpenAI.api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI()
    return client

def generate_response(chunks: list, question: str) -> str:
    messages = [{
        "role": "system",
        "content": "You are a helpful assistant that answers questions. Use the information the user provides to answer the question the user provides."
    },
    {
        "role": "user",
        "content": question
    }]

    for chunk in chunks:
        messages.append({"role": "user", "content": chunk})

    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )
    
    return response.choices[0].message.content
    
# print(generate_response(
#     [
#         "AE is een consultancy bedrijf in Leuven",
#         "AE onderneemt allerlei IT projecten voor klanten in heel België",
#         "AE heeft 320 werknemers"
#     ],
#     "Hoeveel werknemers heeft AE?"
# ))