from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import asyncio

from services.schemas import AggregationRequest
from services.get_aggregated_data import form_aggregation

router = Router()

@router.message(Command("start"))
async def get_start(message: Message):
    await message.answer('Hi!')


@router.message()
async def aggregate(message: Message):
    try:
        case = AggregationRequest(message.text)
    except Exception as ex:
        raise ex
    
    response = form_aggregation()

    await message.answer(response)
