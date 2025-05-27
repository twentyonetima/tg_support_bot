from sqlalchemy import Column, Integer, BigInteger, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base
import enum

class ReplyModeEnum(str, enum.Enum):
    thread = "thread"
    simple = "simple"

class MessageMap(Base):
    __tablename__ = "message_map"

    id: Mapped[int] = mapped_column(primary_key=True)
    support_message_id: Mapped[int] = mapped_column(unique=True, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    user_message_id: Mapped[int] = mapped_column()
    chat_id: Mapped[int] = mapped_column(BigInteger)
    user_display_name: Mapped[str] = mapped_column()
    reply_mode: Mapped[ReplyModeEnum] = mapped_column(default=ReplyModeEnum.simple)