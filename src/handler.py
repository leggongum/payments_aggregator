from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import pydantic_core

import asyncio
import json

from services.schemas import AggregationRequest
from services.get_aggregated_data import form_aggregation

router = Router()

@router.message(Command("start"))
async def get_start(message: Message):
    await message.answer('Hi!')


@router.message()
async def aggregate(message: Message):
    try:
        case = AggregationRequest(**json.loads(message.text))
    except json.decoder.JSONDecodeError:
        return await message.answer('Принимаются только сообщения вида: \n{\n"dt_from": isodate,\n"dt_upto": isodate,\n"group_type":"hour" or "day" or "week" or "month"\n}')
    except pydantic_core._pydantic_core.ValidationError:
        return await message.answer('Принимаются только сообщения вида: \n{\n"dt_from": isodate,\n"dt_upto": isodate,\n"group_type":"hour" or "day" or "week" or "month"\n}')
    except TypeError:
        return await message.answer('Принимаются только сообщения вида: \n{\n"dt_from": isodate,\n"dt_upto": isodate,\n"group_type":"hour" or "day" or "week" or "month"\n}')

    response = form_aggregation(case.model_dump())

    await message.answer(response)
