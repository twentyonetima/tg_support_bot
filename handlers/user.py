from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import SUPPORT_CHAT_ID
from services.state import reply_map, user_names
from services.utils import get_user_display_name

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здравствуйте! Напишите ваш вопрос, и мы скоро ответим.")

async def user_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    user = msg.from_user
    user_id = user.id

    user_names[user_id] = get_user_display_name(user)
    text = f"📩 Сообщение от {user_names[user_id]} (ID: {user_id}):\n\n{msg.text}"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Ответить в треде", callback_data="reply_mode:{}:thread"),
            InlineKeyboardButton("Ответить отдельным сообщением", callback_data="reply_mode:{}:simple"),
        ]
    ])

    sent = await context.bot.send_message(chat_id=SUPPORT_CHAT_ID, text=text)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Ответить в треде", callback_data=f"reply_mode:{sent.message_id}:thread"),
            InlineKeyboardButton("Ответить отдельным сообщением", callback_data=f"reply_mode:{sent.message_id}:simple"),
        ]
    ])
    await context.bot.edit_message_reply_markup(chat_id=SUPPORT_CHAT_ID, message_id=sent.message_id, reply_markup=keyboard)

    reply_map[sent.message_id] = {
        "user_id": user_id,
        "user_message_id": msg.message_id,
        "chat_id": msg.chat.id,
    }
