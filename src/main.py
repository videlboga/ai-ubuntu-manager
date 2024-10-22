import sys
from ai_interface import ask_openrouter
from command_executor import run_command
from logger import setup_logger

logger = setup_logger()

def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Мур-мяу! Введите ваш запрос, братишка: ")

    logger.info(f"Получен запрос: {query}")
    response = ask_openrouter(f"Сгенерируй команду для Ubuntu, чтобы {query}. Верни только команду, без дополнительных пояснений.")

    if 'choices' in response and len(response['choices']) > 0:
        command = response['choices'][0]['message']['content'].strip()
        logger.info(f"Сгенерированная команда: {command}")
        print(f"Мур-мяу! Вот команда, которую я сгенерировал, братишка: {command}")
        confirm = input("Выполнить эту команду? (y/n): ")
        if confirm.lower() == 'y':
            result = run_command(command)
            logger.info(f"Результат выполнения: {result}")
            print("Мур-мяу! Вот результат выполнения команды, братишка:")
            print(result)
        else:
            print("Мур-мяу! Команда не была выполнена, братишка.")
    else:
        logger.error("Не удалось получить ответ от AI")
        print("Мур-мяу! Извини, братишка, но я не смог получить ответ. Может, попробуем еще раз?")

if __name__ == "__main__":
    main()
