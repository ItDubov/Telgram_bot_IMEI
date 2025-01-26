from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN, AUTHORIZED_USERS
from imei_checker import check_imei


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветствие для пользователя."""
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USERS.values():
        await update.message.reply_text("Доступ запрещен.")
        return
    await update.message.reply_text("Добро пожаловать! Отправьте IMEI для проверки.")


async def handle_imei(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка IMEI."""
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USERS.values():
        await update.message.reply_text("Доступ запрещен.")
        return

    imei = update.message.text.strip()
    if not imei.isdigit() or len(imei) not in [15, 16]:
        await update.message.reply_text("Неверный формат IMEI. Пожалуйста, введите корректный IMEI.")
        return

    result = await check_imei(imei)
    await update.message.reply_text(f"Результат проверки IMEI:\n{result}")


def run_bot():
    """Запускает Telegram-бота."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_imei))

    application.run_polling()
