import requests
import json
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit

API_KEY = "твой_ключ_api"
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UbuntuAssistantGUI()
    ex.show()
    sys.exit(app.exec_())
