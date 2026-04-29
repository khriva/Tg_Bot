from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database.db import generate_student_id, get_teacher_by_id
start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Ты учитель или ученик?')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Учитель 👩‍🏫", callback_data="role_teacher"),
            InlineKeyboardButton(text="Ученик 🤓",callback_data ="role_student") ]
            ]
    )
    await message.answer("Who are you, my friend ?", reply_markup=keyboard)