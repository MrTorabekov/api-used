import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import requests

from config import TOKEN

dp = Dispatcher()


class Form(StatesGroup):
    currency1 = State()  # fromCurrency
    currency2 = State()  # toCurrency
    amount = State()  # qiymat  # noqa
    finish = State()  # finish


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(f"<b>Assalomu Aleykum {message.from_user.mention_html()}</b>")
    await state.set_state(Form.currency1)
    await message.answer("<b>Qaysi valyutadan convertatsiya qilmoqchisiz ❓</b>")


@dp.message(Form.currency1)
async def currency1(message: types.Message, state: FSMContext):
    await state.update_data(currency1=message.text.upper())
    await state.set_state(Form.currency2)
    await message.answer("<b>Qaysi valyutaga convertatsiya qilmoqchisiz ❓</b>")


@dp.message(Form.currency2)
async def currency2(message: types.Message, state: FSMContext):
    await state.update_data(currency2=message.text.upper())
    await state.set_state(Form.amount)
    await message.answer("<b>Miqdorni kiriting:</b>")


@dp.message(Form.amount)
async def amount(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(amount=message.text)
    await state.set_state(Form.finish)
    data = await state.get_data()
    await state.clear()
    delete = await message.answer(f"<b>Biroz kuting....</b>")  # noqa
    currency1 = data.get("currency1", "Unknown")
    currency2 = data.get("currency2", "Unknown")
    amount = data.get("amount", "Unknown")

    url = "https://fast-currency-convertor.p.rapidapi.com/api/Fetch-Currency/"

    querystring = {"amount": f"{amount}", "fromCurrency": f"{currency1}", "toCurrency": f"{currency2}"}

    headers = {
        "X-RapidAPI-Key": "5560fa2df7msh4b8bb710dddd43fp1697ddjsn65d80adca939",
        "X-RapidAPI-Host": "fast-currency-convertor.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    result = response.json()
    # print(result.get("value"))
    msg = f"""<b>
Qaysi summadan: {currency1}    
Qaysi summaga: {currency2}
Miqdor : {amount}
Natija: {result.get("value", "None")}</b>
"""
    await bot.delete_message(chat_id=message.chat.id, message_id=delete.message_id)
    await bot.send_message(chat_id=message.chat.id, text=msg)
