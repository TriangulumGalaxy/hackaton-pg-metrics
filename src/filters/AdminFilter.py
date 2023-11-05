from typing import Any
from aiogram.filters import Filter
from aiogram.types import Message


class IsAdmin(Filter):
    def __init__(self, admins: list) -> None:
        self.admins = admins

    async def __call__(self, message: Message) -> bool:
        print(message.from_user.id in self.admins, message.from_user.id, self.admins)
        return message.from_user.id in self.admins
