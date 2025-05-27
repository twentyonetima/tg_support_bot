from telegram import Update
from telegram.ext import ContextTypes
from database.base import AsyncSessionLocal
from database.crud import set_reply_mode
from database.models import ReplyModeEnum


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        _, msg_id_str, mode_str = query.data.split(":")
        msg_id = int(msg_id_str)
        mode = ReplyModeEnum(mode_str)
    except Exception:
        await query.edit_message_text("Ошибка обработки выбора.")
        return

    async with AsyncSessionLocal() as session:
        await set_reply_mode(session, msg_id, mode)

    await query.edit_message_text(
        f"Выбран режим ответа: {'в треде' if mode == ReplyModeEnum.thread else 'отдельным сообщением'}.\nТеперь ответьте на данное сообщение."
    )
