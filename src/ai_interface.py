import requests
import json
from config import API_KEY, API_BASE, MODEL
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from system_info import get_system_info

def ask_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    system_info = get_system_info()
    formatted_prompt = USER_PROMPT_TEMPLATE.format(user_input=prompt, system_info=system_info)
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": formatted_prompt}
        ]
    }
    response = requests.post(API_BASE, headers=headers, json=data)
    return response.json()
