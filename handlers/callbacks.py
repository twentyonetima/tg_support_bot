from telegram import Update
from telegram.ext import ContextTypes
from services.state import reply_mode_map

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    try:
        prefix, msg_id_str, mode = data.split(":")
        msg_id = int(msg_id_str)
    except Exception:
        await query.edit_message_text("Ошибка обработки выбора режима ответа.")
        return

    if prefix != "reply_mode" or mode not in ("thread", "simple"):
        await query.edit_message_text("Неверный выбор.")
        return

    reply_mode_map[msg_id] = mode
    mode_text = "в треде (reply)" if mode == "thread" else "отдельным сообщением"
    await query.edit_message_text(
        f"Выбран режим ответа: {mode_text}\nТеперь ответьте на данное сообщение в этом чате."
    )
