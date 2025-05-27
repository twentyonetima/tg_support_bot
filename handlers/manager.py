from telegram import Update
from telegram.ext import ContextTypes
from database.base import AsyncSessionLocal
from database.crud import get_message_map
from logs import logger


async def manager_reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg.reply_to_message:
        return

    original_id = msg.reply_to_message.message_id

    async with AsyncSessionLocal() as session:
        info = await get_message_map(session, support_msg_id=original_id)

    if not info:
        logger.warning("Нет данных по сообщению %s", original_id)
        return

    try:
        if info.reply_mode == "thread":
            await context.bot.send_message(chat_id=info.chat_id, text=msg.text, reply_to_message_id=info.user_message_id)
        else:
            await context.bot.send_message(chat_id=info.chat_id, text=msg.text)

        logger.info("Ответ отправлен пользователю %s (режим %s)", info.user_id, info.reply_mode)
    except Exception as e:
        logger.error("Ошибка при отправке: %s", e)