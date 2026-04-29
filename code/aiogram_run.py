import asyncio
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from handlers.student_buttons  import student_router
from database.db import init_db
from handlers.teacher_buttons import teacher_router
from handlers.admin_buttons import admin_router


async def main():
    dp.include_router(start_router)
    dp.include_router(student_router)
    dp.include_router(teacher_router)
    dp.include_router(admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == "__main__":
    init_db()
    asyncio.run(main())

