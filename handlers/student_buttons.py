from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database.db import generate_student_id, get_teacher_by_id,get_all_teachers,occupy_teacher_id
from database.db import add_student
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
student_router = Router()

class StudentStates(StatesGroup):
    waiting_for_teacher = State()
    waiting_for_name = State()


@student_router.callback_query(lambda c: c.data == "role_student")
async def option1_callback(callback: types.CallbackQuery,state : FSMContext):
    await callback.answer()
    await callback.message.answer("Как тебя зовут ?")
    await state.set_state(StudentStates.waiting_for_name)

@student_router.message(StudentStates.waiting_for_name)
async def receive_name(message: types.Message,state: FSMContext):
    await state.update_data(student_name=message.text)
    await message.answer("Какой id у твоего учителя ?")
    await state.set_state(StudentStates.waiting_for_teacher)

@student_router.message(StudentStates.waiting_for_teacher)
async def receive_teacher(message: types.Message, state: FSMContext):
    await state.update_data(teacher_id=int(message.text))
    await state.update_data(tg_id=int(message.from_user.id))
    await state.update_data(student_id= generate_student_id())
    teacher_name = get_teacher_by_id(message.text)
    if teacher_name:
        await message.answer(f"Это твой учитель? {teacher_name}")
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Да ✅", callback_data="yes, teacher exists"),
                    InlineKeyboardButton(text="Нет ❌", callback_data="no, teacher doesnt exist")
                ]
            ]
        )
        await message.answer("?",reply_markup=keyboard)
    else:
        await message.answer("Такого учителя не существует, попробуй еще раз")
        await state.set_state(StudentStates.waiting_for_teacher)


@student_router.callback_query(lambda c: c.data =="yes, teacher exists")
async def student_response(callback: CallbackQuery, state: FSMContext):
    if callback.data == "yes, teacher exists":
        await callback.answer("Ученик подтвержден ✅")
        data = await state.get_data()
        add_student(data["tg_id"], data["student_name"],data["teacher_id"], data["student_id"])
        await callback.message.answer("Регистрация завершена!")
        await state.clear()
        return
    else:
        await callback.answer("Попробуй снова ❌")
        await callback.message.answer("Введи ID учителя ещё раз:")
        await state.set_state(StudentStates.waiting_for_teacher)
