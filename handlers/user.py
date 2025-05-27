from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import SUPPORT_CHAT_ID
from database.base import AsyncSessionLocal
from database.crud import save_message_map
from services.utils import get_user_display_name
from services.i18n import get_user_language, get_text, language_selection_markup


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_lang = get_user_language(update)
    greeting = get_text(user_lang, "greeting_select")
    keyboard = language_selection_markup()
    await update.message.reply_text(greeting, reply_markup=keyboard)


async def language_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if not data.startswith("set_lang:"):
        await query.edit_message_text("Ошибка выбора языка.")
        return

    lang = data.split(":")[1]
    context.user_data["lang"] = lang

    prompt = get_text(lang, "prompt_question")
    await query.edit_message_text(prompt)


async def user_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", get_user_language(update))
    msg = update.effective_message
    user = msg.from_user
    user_id = user.id
    display_name = get_user_display_name(user)

    text = f"📩 Сообщение от {display_name} (ID: {user_id}):\n\n{msg.text}"
    sent = await context.bot.send_message(chat_id=SUPPORT_CHAT_ID, text=text)

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Ответить в треде", callback_data=f"reply_mode:{sent.message_id}:thread"),
        InlineKeyboardButton("Ответить отдельным сообщением", callback_data=f"reply_mode:{sent.message_id}:simple"),
    ]])
    await context.bot.edit_message_reply_markup(SUPPORT_CHAT_ID, sent.message_id, reply_markup=keyboard)

    async with AsyncSessionLocal() as session:
        await save_message_map(
            session,
            support_msg_id=sent.message_id,
            user_id=user_id,
            user_msg_id=msg.message_id,
            chat_id=msg.chat.id,
            display_name=display_name,
        )