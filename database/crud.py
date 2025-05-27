from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import MessageMap, ReplyModeEnum

async def save_message_map(session: AsyncSession, *, support_msg_id, user_id, user_msg_id, chat_id, display_name):
    db_obj = MessageMap(
        support_message_id=support_msg_id,
        user_id=user_id,
        user_message_id=user_msg_id,
        chat_id=chat_id,
        user_display_name=display_name
    )
    session.add(db_obj)
    await session.commit()

async def get_message_map(session: AsyncSession, support_msg_id: int) -> MessageMap | None:
    result = await session.execute(select(MessageMap).where(MessageMap.support_message_id == support_msg_id))
    return result.scalars().first()

async def set_reply_mode(session: AsyncSession, support_msg_id: int, mode: ReplyModeEnum):
    await session.execute(
        update(MessageMap)
        .where(MessageMap.support_message_id == support_msg_id)
        .values(reply_mode=mode)
    )
    await session.commit()