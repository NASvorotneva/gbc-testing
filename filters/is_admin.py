from typing import Union

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery

from data.config import ADMINS


class AdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message_or_call: Union[Message, CallbackQuery]):
        return message_or_call.from_user.id in ADMINS
