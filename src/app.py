from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update

from fastapi import FastAPI, Request

from config import settings


bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

from handler import router
dp.include_router(router)


async def on_startup():
    await bot.set_webhook(url=settings.WEBAPP_URL)

app = FastAPI(on_startup=[on_startup])

@app.post('/')
async def webhook(request: Request):
    update = Update.model_validate(await request.json(), context={'bot': bot})
    await dp.feed_update(bot, update)
    