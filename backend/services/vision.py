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
    prompt = """This is a screenshot the user took.
First, determine if this is a medical exam/study question with a clear correct answer.

If it IS a medical question, return JSON only, no markdown:
{
  "is_question": true,
  "question": "the full question text, preserved verbatim with all clinical details (patient age, sex, symptoms, vitals, lab values, history). Do not summarize or paraphrase.",
  "correct_answer": "the correct answer option letter and full text exactly as written",
  "explanation": "the full explanation from the question bank, preserving clinical reasoning and key details. Do not over-condense.",
  "anki_front": "the question as written, keeping the clinical vignette intact. Include the patient presentation, key findings, and the actual question being asked. Do not collapse the vignette into a single short sentence.",
  "anki_back": "the correct answer with the full clinical reasoning. Include why this answer is correct AND briefly why the other key distractors are wrong if mentioned. Should be thorough enough to actually learn from, not just memorize."
}

If it is NOT a medical question (e.g., a random screenshot, chat, webpage), return:
{
  "is_question": false,
  "reason": "brief explanation of what the image actually is"
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
    
    if not content:
        # Model returned empty — likely rate limited or filtered
        raise Exception("Model returned empty response. Try again or switch models.")
    
    content = content.replace("```json", "").replace("```", "").strip()
    
    # Find first { and last } to extract JSON even if there's surrounding text
    start = content.find("{")
    end = content.rfind("}")
    if start != -1 and end != -1:
        content = content[start:end+1]
    
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return json.loads(content, strict=False)