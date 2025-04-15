from openai import OpenAI
from typing import List, Optional
import re
import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel, field_validator

load_dotenv()

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENAI_API_KEY"))

class ParsedCommand(BaseModel):
    site: str
    action: List[str]
    search_item: str
    match_keyword: Optional[str]

    @field_validator('site')
    def lowercase_site(cls, value):
        return value.lower()


def parsed_ai_cmd(user_input: str) -> dict:
    prompt = parser_prompt(user_input)

    response = client.chat.completions.create(
        model = "openai/gpt-3.5-turbo:free",
        messages = [{"role":"user", "content": prompt}], 
        temperature = 0.1
    )

    try:
        output = response.choices[0].message.content
        clean_output = re.sub(r"^```(?:json)?\s*|```$", "", output.strip(), flags=re.MULTILINE)
        json_data = json.loads(clean_output)
        # Unpacking dict with **
        return ParsedCommand(**json_data).model_dump()
    except Exception as e:
        return {"error":str(e)}

def parser_prompt(user_input):
    prompt = f'''
    
You are an intelligent command parser for a browser automation agent.

Extract the following fields from the user command and return them in JSON format (no markdown or backticks):
- site: The ecommerce website mentioned (e.g., amazon, ebay)
- action: One or more actions from ["login", "search", "add_to_cart"] (Actions can be multiple) (as a list of string) 
- search_item: The text to search on the site (e.g. Laptop, Cover, Mobile)
- match_keyword: The keyword used to find the specific best matching result(e.g. Asus ROG Strix G15, 15.6 inch, Apple, Samsung) (This are item features)

Command: {user_input}

 '''
    return prompt


def parse_command(text: str) -> dict:
    return parsed_ai_cmd(text)