from telegram import Update
from telegram.ext import ContextTypes
from services.state import reply_map, reply_mode_map
from logs import logger

async def manager_reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message

    if not msg.reply_to_message:
        return

    original_message_id = msg.reply_to_message.message_id
    info = reply_map.get(original_message_id)

    if not info:
        logger.warning("Нет данных для ответа на сообщение %s", original_message_id)
        return

    user_id = info["user_id"]
    user_message_id = info["user_message_id"]
    chat_id = info["chat_id"]
    mode = reply_mode_map.get(original_message_id, "simple")

    try:
        if mode == "thread":
            await context.bot.send_message(chat_id=chat_id, text=msg.text, reply_to_message_id=user_message_id)
        else:
            await context.bot.send_message(chat_id=chat_id, text=msg.text)

        logger.info("Ответ менеджера отправлен в чат %s пользователю %s (режим %s)", chat_id, user_id, mode)
    except Exception as e:
        logger.error("Ошибка при отправке сообщения пользователю: %s", e)
