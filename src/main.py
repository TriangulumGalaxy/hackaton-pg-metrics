import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from filters import IsAdmin
from db import get_data, add_admin, delete_admin, add_banned_query
from metrics import get_metrics, get_long_queries

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
DB_NAME = getenv('DB_NAME')
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv('DB_PASSWORD')
DB_CRED = (DB_NAME, DB_USER, DB_PASSWORD)

dp = Dispatcher()


@dp.message(IsAdmin(get_data()['admins']), CommandStart())
async def command_start_handler(message: Message) -> None:
    with open('info.txt', encoding='utf-8') as m:
        await message.answer(m.read())


@dp.message(IsAdmin(get_data()['admins']), Command("longq", prefix='/'))
async def command_long_handler(message: Message):
    data = get_long_queries(*DB_CRED)[0]
    await message.answer(f'runtime: {data[0]}\ndatname: {data[1]}\nusename: {data[2]}\nquery: {data[3]}', parse_mode='html')


@dp.message(IsAdmin(get_data()['admins']), Command("info", prefix='/'))
async def command_info_handler(message: Message):
    data = get_metrics(*DB_CRED)
    for line in data:
        # print(line)
        mt = f"datid: {line['datid']}\ndatname: {line['datname']}\nusename: {line['usename']}\napplication_name: {line['application_name']}\nclient_addr: {line['client_addr']}\nclient_hostname: {line['client_hostname']}\nclient_port: {line['client_port']}\nbackend_start: {line['backend_start']}\nxact_start: {line['xact_start']}\nquery_start: {line['query_start']}\nstate_change: {line['state_change']}\nwait_event_type: {line['wait_event_type']}\nwait_event: {line['wait_event']}\nstate: {line['state']}\nbackend_type: {line['backend_type']}\nquery: {line['query']}"
        # mt = mt.replace('-', '\-').replace('.', '\.').replace('+', '\+').replace('(', '\(').replace(')', '\)')
        await message.answer(mt, parse_mode='html')


@dp.message(IsAdmin(get_data()['admins']), Command("admin", prefix='/'))
async def add_user_handler(message: Message):
    uid = message.text.split()[1]
    try:
        add_admin(uid)
    except Exception as E:
        await message.reply('Данные не корректны❌')
        return
    await message.reply('Пользователь добавлен✅')


@dp.message(IsAdmin(get_data()['admins']), Command("delAdmin", prefix='/'))
async def delete_admin_handler(message: Message):
    admin = message.text.split()[1]
    if delete_admin(admin):
        await message.reply('Админ успешно удален✅')
        return
    await message.reply('Не удалось найти админа с указанным ID❌')


@dp.message(IsAdmin(get_data()['admins']), Command("query", prefix='/'))
async def command_query_handler(message: Message):
    q = " ".join(message.text.split()[1:])
    try:
        add_banned_query(q)
        await message.reply('Запрос добавлен✅')
    except Exception as E:
        await message.reply('Не удалось добавить запрос❌')


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())