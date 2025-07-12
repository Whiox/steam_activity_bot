import asyncio
import html
import os

import logging


os.makedirs("logs", exist_ok=True)
logger = logging.getLogger(__name__)

logging.basicConfig(
    filename='logs/app.log',
    level=logging.DEBUG,
    format='[%(asctime)s][%(levelname)s]: %(message)s'
)

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.parser import AccountParser

from src.save import get_games, get_username, get_last_2_week, get_recent_game

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
CHECK_INTERVAL = 10

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(token=TOKEN)
ap = AccountParser()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    logger.info(f"User {message.from_user.id} started command start")

    ap.update()

    games = get_games()
    response = f"Активность пользователя <b>{html.escape(get_username())}</b>\n\n"

    response += f"<code>{html.escape(str(get_last_2_week()))}Ч</code>   <b>за последние две недели</b>\n\n"

    for game in games:
        for name, time in game.items():
            response += f"<b>{html.escape(name)}</b>:   <code>{html.escape(time)}Ч</code>\n"

    await message.answer(response, parse_mode=ParseMode.HTML)


async def compare_recent_game_loop():
    logger.info(f"Next it")
    last = get_recent_game()

    if not last:
        ap.update()
        last = get_recent_game()

    while True:
        await asyncio.sleep(CHECK_INTERVAL)

        ap.update()
        new = get_recent_game()

        (name, hours), = last.items()
        (name_, hours_), = new.items()

        if name != name_:
            logger.info(f"New game found")

            text = (
                f"<b>Новая активность {html.escape(get_username())}</b>\n\n"
                f"<b>{html.escape(str(name_))}</b>: <code>{html.escape(str(hours_))}Ч</code>"
            )
            await bot.send_message(CHAT_ID, text)

        else:
            logger.info(f"No new game found")

        new = get_recent_game()
        last = new.copy()


async def main() -> None:
    logger.info("Creating loop task...")
    asyncio.create_task(compare_recent_game_loop())

    logger.info("Starting polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Starting bot...")

    asyncio.run(main())
