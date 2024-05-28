from aiogram import Router
from aiogram.filters import CommandStart, ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.types import Message, ChatMemberUpdated

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, db):
    await db.sql_create_user(
        user_id=message.from_user.id,
        username=message.from_user.username or '',
        fullname=message.from_user.first_name or '',
        is_active=True
    )


@user_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=KICKED)
)
async def user_blocked_bot(event: ChatMemberUpdated, db):
    await db.sql_update_user_status(is_active=False, user_id=event.from_user.id)


@user_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=MEMBER)
)
async def user_unblocked_bot(event: ChatMemberUpdated, db):
    await db.sql_update_user_status(is_active=True, user_id=event.from_user.id)
