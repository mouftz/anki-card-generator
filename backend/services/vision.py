import os
import json
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generate_anki_card(image_base64: str) -> dict:
    prompt = """This is a screenshot of a medical exam question the user got wrong.
Extract the following and return as JSON only, no markdown, no backticks:
{
  "question": "the full question text",
  "correct_answer": "the correct answer option and its text",
  "explanation": "the explanation for why this is correct",
  "anki_front": "a concise question for the front of the anki card",
  "anki_back": "a concise answer + key explanation for the back of the card"
}"""

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    
    content = response.choices[0].message.content
    # Strip markdown fences and find the JSON object
    content = content.replace("```json", "").replace("```", "").strip()
    
    # Find first { and last } to extract JSON even if there's surrounding text
    start = content.find("{")
    end = content.rfind("}")
    if start != -1 and end != -1:
        content = content[start:end+1]
    
    return json.loads(content)