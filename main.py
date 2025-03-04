import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command, StateFilter
from aiogram.enums import ParseMode

from loguru import logger

from classes.user_status import UserStatus
from config import BOT_TOKEN
from handlers.game_handler import GameHandler

logger.add("logfile.log", level="DEBUG")

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp.message.register(GameHandler.start_command, Command(commands=["start"]))
dp.message.register(GameHandler.start_command, F.text == "Вернуться обратно", UserStatus.approving_deck)
dp.message.register(GameHandler.start_command, F.text == "Завершить сессию", StateFilter(UserStatus.session_front, UserStatus.session_back))
dp.message.register(GameHandler.approve_deck, UserStatus.picking_deck)
dp.message.register(GameHandler.start_session, F.text == "Да", UserStatus.approving_deck)
dp.message.register(GameHandler.show_back, F.text == "Перевернуть", UserStatus.session_front)
dp.message.register(GameHandler.check_answer_and_show_next_card, F.text.in_(["Знаю", "Повторить"]), UserStatus.session_back)

async def main() -> None:
	await dp.start_polling(bot)


asyncio.run(main())