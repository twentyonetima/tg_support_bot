from telegram import InlineKeyboardMarkup, InlineKeyboardButton

LANGUAGES = {
    "ru": {
        "greeting_select": "Здравствуйте, выберите язык",
        "prompt_question": "Напишите ваш вопрос, и мы скоро ответим.",
        "language_name": "Русский",
    },
    "en": {
        "greeting_select": "Hello, please select a language.",
        "prompt_question": "Write your question and we will answer soon.",
        "language_name": "English",
    }
}

LANG_BUTTONS = [
    InlineKeyboardButton(text=LANGUAGES["ru"]["language_name"], callback_data="set_lang:ru"),
    InlineKeyboardButton(text=LANGUAGES["en"]["language_name"], callback_data="set_lang:en"),
]

def get_user_language(update) -> str:
    user_lang = getattr(update.effective_user, "language_code", None)
    if user_lang and user_lang.startswith("ru"):
        return "ru"
    return "en"

def get_text(lang: str, key: str) -> str:
    return LANGUAGES.get(lang, LANGUAGES["en"]).get(key, "")

def language_selection_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([LANG_BUTTONS])