from fastapi import FastAPI, APIRouter
from config import config
import json
import os

from openai import AzureOpenAI

from models.askmodel import Question

askRouter = APIRouter()

# ✅ Get absolute path to config/qa_data.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
json_path = os.path.join(BASE_DIR, "config", "qa_data.json")

# ✅ Load JSON once
with open(json_path, "r", encoding="utf-8") as f:
    qa_data = json.load(f)



client = AzureOpenAI(
    api_version=config.config.azure_openai_api_version,
    azure_endpoint=config.config.azure_openai_endpoint,
    api_key=config.config.openai_api_key,
)


@askRouter.post("/ask")
async def ask_question(item: Question):
    user_question = item.query.strip()

    # 1. Exact match
    if user_question in qa_data:
        return {"answer": qa_data[user_question]}

    # 2. Use Azure OpenAI for related questions
    response = client.chat.completions.create(
        model=config.config.azure_openai_deployment,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a supportive health advisor for teenagers. "
                    "Answer only questions related to smoking, nicotine, and their effects on teens "
                    "(addiction, academics, social pressures, growth, athletics,financial). "
                    "If the question is unrelated, politely explain you cannot answer."
                )
            },
            {"role": "user", "content": user_question}
        ],
        max_tokens=250
    )

    ai_answer = response.choices[0].message.content

    # 3. Custom message if Azure AI says it's unrelated
    if "cannot answer" in ai_answer.lower():
        return {"answer": "Sorry, I can only answer smoking-related health questions for teenagers."}
    print("----------------------------------")
    print(ai_answer)
    return {"answer": ai_answer}
