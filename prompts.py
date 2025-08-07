# prompts.py
import os
from dotenv import load_dotenv
import openai

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)
print("🔍 API KEY =", api_key)

def generate_drug_info(input_text, mode="drug"):
    if mode == "condition":
        # Simple list of 5 drug names for the condition
        system_prompt = "You are a helpful pharmacist. Just return a clean list of 5 drug names that are commonly used to treat the given condition."
        user_prompt = f"List 5 commonly used medications to treat {input_text}. Only return the drug names in bullet points starting with dashes."
    else:
        # Detailed response about a specific drug
        system_prompt = (
            "You are a helpful medical assistant. When given a drug name, respond in the following format:\n\n"
            "**What is it used for?**\n"
            "(Short paragraph)\n\n"
            "**Common side effects**\n"
            "- list 5–6 as bullet points\n\n"
            "**Precautions**\n"
            "- list 4–5 bullet points\n\n"
            "**Summary**\n"
            "(Short paragraph)\n\n"
            "Use clean markdown. Only return these 4 sections, with bold headings exactly as shown above."
        )
        user_prompt = f"Drug: {input_text}"

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"
