from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import asyncio

router = Router()

@router.message(Command("start"))
async def get_start(message: Message):
    await message.answer('Привет!')

@router.message()
async def echo(message: Message):
    await message.answer(message.text)
