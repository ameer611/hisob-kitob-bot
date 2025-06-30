from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import keyboards as kb
from database import get_db
from schema import UserOut
from service import get_user_by_tg_id, get_all_users, clear_active_expenses, get_expenses
from settings import settings

router = Router()

@router.message(F.text == "Hisobot🧾")
async def handle_expense(message: Message, state: FSMContext):
    """
    Handle the user's expense input.
    """
    gen = get_db()
    db = await anext(gen)
    try:
        user_db = await get_user_by_tg_id(db, message.from_user.id)
        if not user_db:
            await message.answer("Iltimos, avval ro'yxatdan o'ting (/register).")
            return
        users = await get_all_users(db)
        if not users:
            await message.answer("Hozirda hech kim ro'yxatdan o'tmagan.")
            return

        active_expenses = await get_expenses(db)
        sum_amount_expenses = 0

        if active_expenses:
            await message.answer("Sizning faol sarflaringiz:")
            for expense in active_expenses:
                sum_amount_expenses += expense.amount
                await message.answer(
                    f"Sarflovchi ismi: {expense.user.name}\n"
                    f"Sarflangan summa: {expense.amount} so'm\n"
                    f"Sarf sababi: {expense.description}\n"
                    f"Sarflangan vaqt: {expense.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                )
        else:
            await message.answer("Sizda faol sarflar mavjud emas.")

        average_expense = sum_amount_expenses / len(users) if users else 0
        return_message = (
            f"Jami sarflangan summa: {sum_amount_expenses} so'm\n"
            f"O'rtacha sarf: {average_expense:.2f} so'm\n\n"
        )

        for user in users:
            user = UserOut.model_validate(user)
            sum_expense_of_user = user.sum_expenses if user.sum_expenses else 0

            return_message += (
                f"Foydalanuvchi: {user.name}, "
                f"Sarflangan summa: {sum_expense_of_user} so'm\n"
            )

            if sum_expense_of_user > average_expense:
                return_message += (
                    f"{user.name} {sum_expense_of_user-average_expense:.2f} so'm haqdor.\n\n"
                )
            elif sum_expense_of_user < average_expense:
                return_message += (
                    f"{user.name} {average_expense-sum_expense_of_user:.2f} so'm qarzdor.\n\n"
                )
            else:
                return_message += f"{user.name} qarz yoki haqdor emas.\n\n"

        await message.answer(return_message, reply_markup=kb.calculated_kb)
    finally:
        await gen.aclose()

@router.callback_query(F.data == "calculated")
async def calculated_callback(callback: CallbackQuery):
    """
    Handle the callback for the calculated button.
    """
    # Corrected admin check
    if int(callback.from_user.id) not in settings.admin_users_ids:
        await callback.answer("Bu amalni faqat adminlar bajarishi mumkin.", show_alert=True)
        return

    await callback.answer("Hisob-kitob qilindi, barcha sarflar o'chiriladi!", show_alert=True)
    await callback.message.edit_text("Hisob-kitob qilindi!", reply_markup=None)

    # Correct use of async generator for DB session
    gen = get_db()
    db = await anext(gen)
    try:
        rows = await clear_active_expenses(db)
    finally:
        await gen.aclose()

    if rows:
        await callback.message.answer(f"{rows} ta faol sarf ma'lumotlari o'chirildi.")
    else:
        await callback.message.answer("Faol sarf ma'lumotlari topilmadi.")