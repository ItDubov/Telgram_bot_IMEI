import uvicorn
from multiprocessing import Process
from telegram_bot import run_bot
from main import app


def start_api():
    """Функция для запуска FastAPI."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


def start_telegram_bot():
    """Функция для запуска Telegram-бота."""
    run_bot()


if __name__ == "__main__":
    # Запускаем API и Telegram-бота параллельно
    api_process = Process(target=start_api)
    telegram_process = Process(target=start_telegram_bot)

    api_process.start()
    telegram_process.start()

    api_process.join()
    telegram_process.join()
