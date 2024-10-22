import urllib.request
import urllib.parse
import sys
import locale
import requests
import json
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit
from config import API_KEY

# Устанавливаем локаль по умолчанию
locale.setlocale(locale.LC_ALL, '')

# Устанавливаем кодировку по умолчанию для sys.stdout
sys.stdout.reconfigure(encoding='utf-8')


API_BASE = "https://openrouter.ai/api/v1/chat/completions"

class UbuntuAssistantGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        self.input_field = QLineEdit()
        self.output_area = QTextEdit()
        self.send_button = QPushButton('Отправить запрос')
        self.confirm_button = QPushButton('Выполнить команду')
        
        layout.addWidget(self.input_field)
        layout.addWidget(self.send_button)
        layout.addWidget(self.output_area)
        layout.addWidget(self.confirm_button)
        
        self.setLayout(layout)
        self.setWindowTitle('Кибер-котенок Ассистент для Ubuntu')
        
        self.send_button.clicked.connect(self.send_request)
        self.confirm_button.clicked.connect(self.confirm_action)
        
    def send_request(self):
        query = self.input_field.text()
        response = ask_openrouter(f"Сгенерируй команду для Ubuntu, чтобы {query}. Верни команду и краткое объяснение, что она делает.")
        if 'choices' in response and len(response['choices']) > 0:
            self.command = response['choices'][0]['message']['content'].strip()
            self.output_area.setText(f"Предлагаемая команда:\n{self.command}\n\nПодтвердите выполнение.")
        else:
            self.output_area.setText("Не удалось получить ответ.")
        
    def confirm_action(self):
        result = execute_command(self.command)
        self.output_area.append(f"\n\nРезультат выполнения:\n{result}")

import urllib.request
import urllib.parse

def encode_header_value(value):
    return urllib.parse.quote(value.encode('utf-8'))

def ask_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost:3000",
        "X-Title": "Ubuntu Assistant"
    }
    data = {
        "model": "nousresearch/hermes-3-llama-3.1-405b:free",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    print(f"Request URL: {API_BASE}")
    print(f"Request headers: {headers}")
    print(f"Request data: {data}")
    
    encoded_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(API_BASE, data=encoded_data, method='POST')
    for key, value in headers.items():
        req.add_header(key, value)
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Response body: {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Ошибка: {e.stderr}"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UbuntuAssistantGUI()
    ex.show()
    sys.exit(app.exec_())
