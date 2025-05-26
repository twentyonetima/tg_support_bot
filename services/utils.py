from telegram import User

def get_user_display_name(user: User) -> str:
    return f"@{user.username}" if user.username else f"{user.first_name} {user.last_name or ''}".strip()