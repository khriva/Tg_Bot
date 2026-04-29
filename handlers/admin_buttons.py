from random import setstate

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database.db import generate_student_id, get_teacher_by_id, occupy_teacher_id,get_all_teachers,reserve_teacher_id
from database.db import add_student
from aiogram.types import CallbackQuery
ADMIN_ID=1120733634
admin_router = Router()
class AdminStates(StatesGroup):
    waiting_for_teacher = State()

@admin_router.message(Command("admin"))
async def cmd_start(message: Message):
    if int(message.from_user.id) == ADMIN_ID:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Просмотреть учителей", callback_data="show_teachers"),
                 InlineKeyboardButton(text="Добавить учителя ", callback_data="add_teacher")]
            ]
        )
        await message.answer("прив",reply_markup=keyboard)
    else:
        await message.answer("Отказано в доступе")
@admin_router.callback_query(lambda c: c.data == "show_teachers")
async def show_teachers(callback: types.CallbackQuery,state : FSMContext):
    await callback.answer()
    text = "\n".join(get_all_teachers())
    await callback.message.answer(text)

@admin_router.callback_query(lambda c: c.data == "add_teacher")
async def waiting_for_id(callback: types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await callback.message.answer("Введи id нового учителя")
    await state.set_state(AdminStates.waiting_for_teacher)
@admin_router.message(AdminStates.waiting_for_teacher)
async def add_teacher(message: types.Message,state: FSMContext):
    reserve_teacher_id(int(message.text))
    await state.clear()
    await message.answer("ID зарегистрирован")





        


