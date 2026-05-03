from multiprocessing.connection import answer_challenge

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database.db import generate_student_id, get_teacher_by_id, occupy_teacher_id
from database.db import add_student, show_students
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder



teacher_router = Router()

class TeacherStates(StatesGroup):
    waiting_for_id = State()
    waiting_for_name = State()

class AddHomework(StatesGroup):
    waiting_for_text = State()
    waiting_for_student = State()
@teacher_router.callback_query(lambda c: c.data == "role_teacher")
async def option2_callback(callback: types.CallbackQuery, state = FSMContext):
     await callback.answer()
     await callback.message.answer("Как тебя зовут ?")
     await state.set_state(TeacherStates.waiting_for_name)

@teacher_router.message(TeacherStates.waiting_for_name)
async def receive_name(message: types.Message,state: FSMContext):
    await state.update_data(teacher_name=message.text)
    await message.answer("Какой твой Id ?")
    await state.set_state(TeacherStates.waiting_for_id)

@teacher_router.message(TeacherStates.waiting_for_id)
async def receive_id(message : types.Message,state:FSMContext):
    await state.update_data(teacher_id = int(message.text))
    await state.update_data(tg_id = int(message.from_user.id))
    data = await state.get_data()
    occupy_teacher_id(data["teacher_id"],data["teacher_name"],data["tg_id"])
    await message.answer(occupy_teacher_id(data["teacher_id"],data["teacher_name"],data["tg_id"]))
    await message.answer("Учитель успешно зарегистрирован")
@teacher_router.message(Command("menu"))
async def show_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Просмотреть учеников", callback_data="show_students"),
             InlineKeyboardButton(text="Добавить дз", callback_data="add_hw")]
        ]
    )
    await message.answer("Добрый день", reply_markup=keyboard)

@teacher_router.callback_query(lambda c: c.data == "show_students")
async def get_students(callback: types.CallbackQuery):
    teacher_tg_id =callback.from_user.id
    await callback.answer()
    names =  (show_students(teacher_tg_id))
    if names:
        text = "\n".join([i["full_name"] for i in names])
        await callback.message.answer(text)
    else:
        await callback.message.answer("Список учеников пуст.")

@teacher_router.callback_query(lambda c: c.data == "add_hw")
async def add_hw(callback: types.CallbackQuery, state : FSMContext):
    builder = InlineKeyboardBuilder()
    teacher_tg_id =callback.from_user.id
    await callback.answer()
    students = (show_students(teacher_tg_id))
    for user in students :
        builder.button(
            text=user['full_name'],
            callback_data=f"user_info_{user['student_id']}"
        )
    builder.adjust(1)
    await callback.message.answer("Выберите ученика:", reply_markup=builder.as_markup())
    await state.set_state(AddHomework.waiting_for_student)

@teacher_router.callback_query(AddHomework.waiting_for_student)








