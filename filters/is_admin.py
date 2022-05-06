from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from data.config import ADMINS


class AdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: Message):
        return str(message.from_user.id) in ADMINS
