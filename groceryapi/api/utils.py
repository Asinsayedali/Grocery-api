from groq import Groq
from dotenv import load_dotenv
import os
import json
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def generate_response(prompt,data):
    systemprompt = {
        "role":"system",
        "content":"""
        You are an intelligent recipe generation assistant. Your job is to help users create recipes based on the items they currently have in their kitchen or inventory.

        When given:

        A list of available ingredients (inventory),

        A user query which may include preferences, dietary restrictions, allergies, desired cuisine, or meal type (user_input),

        You must:

        Generate a recipe that only uses the available ingredients or clearly note if a small substitution is needed.

        Respect any dietary restrictions or allergy information strictly.

        Match the user’s preferences, such as vegan, high-protein, quick meals, etc., if mentioned.

        Return the recipe in the following format:

        Title

        Ingredients (quantities if possible)

        Instructions (step-by-step)

        Notes (optional substitutions, preparation tips, or nutrition facts)

        If the inventory is very limited, generate a simple minimal recipe or suggest one or two missing common items that would significantly improve the recipe.

        Do not include ingredients not present in the inventory unless explicitly allowed.
        Always prioritize clarity, creativity, and user safety (allergy handling).

        the output should always be JSON. Dont add any markdown or anything which breaks the code.

"""
    }

    combined = (
        f"Here's the current inventory:\n{data}\n\n"
        f"{prompt}"
    )
    messages = [
        systemprompt,
        {
            "role": "user",
            "content": combined
        }
    ]

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.9,
        top_p=1,
        stream=False,
        stop=None,
    )
    return json.loads(completion.choices[0].message.content)