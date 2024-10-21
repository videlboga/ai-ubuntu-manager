#!/usr/bin/env python3
import requests
import json
import sys
import subprocess
from config import API_KEY

API_BASE = "https://openrouter.ai/api/v1/chat/completions"

def ask_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "anthropic/claude-2",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(API_BASE, headers=headers, data=json.dumps(data))
    return response.json()

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Ошибка: {e.stderr}"

def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Введите ваш запрос: ")

    response = ask_openrouter(f"Сгенерируй команду для Ubuntu, чтобы {query}. Верни только команду, без дополнительных пояснений.")

    if 'choices' in response and len(response['choices']) > 0:
        command = response['choices'][0]['message']['content'].strip()
        print(f"Сгенерированная команда: {command}")
        confirm = input("Выполнить эту команду? (y/n): ")
        if confirm.lower() == 'y':
            result = execute_command(command)
            print("Результат выполнения:")
            print(result)
        else:
            print("Команда не была выполнена.")
    else:
        print("Не удалось получить ответ.")

if __name__ == "__main__":
    main()

