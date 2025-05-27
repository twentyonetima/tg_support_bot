from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import BOT_TOKEN, SUPPORT_CHAT_ID
from handlers.user import user_message_handler, start_command
from handlers.manager import manager_reply_handler
from handlers.callbacks import button_callback
from logs import logger
from database.base import engine, init_models

async def on_startup(app: Application):
    await init_models(engine)
    logger.info("🤖 Все таблицы созданы в БД")
    logger.info("🤖 Бот техподдержки запущен!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.Chat(chat_id=SUPPORT_CHAT_ID)),
        user_message_handler
    ))
    app.add_handler(MessageHandler(
        filters.Chat(chat_id=SUPPORT_CHAT_ID) & filters.REPLY & filters.TEXT,
        manager_reply_handler
    ))
    app.add_handler(CallbackQueryHandler(button_callback, pattern=r"^reply_mode:"))

    app.post_init = on_startup
    app.run_polling()

if __name__ == "__main__":
    main()