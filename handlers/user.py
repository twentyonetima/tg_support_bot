from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import SUPPORT_CHAT_ID
from database.base import AsyncSessionLocal
from database.crud import save_message_map
from services.utils import get_user_display_name


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здравствуйте! Напишите ваш вопрос, и мы скоро ответим.")


async def user_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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