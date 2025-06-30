from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database import get_db
from states import ExpenseStates
from service import get_user_by_tg_id, create_expense

router = Router()

@router.message(F.text == "Pul sarf qildim💸")
async def handle_expense(message: Message, state: FSMContext):
    """
    Handle the user's expense input.
    """
    db = await anext(get_db())
    user_db = await get_user_by_tg_id(db, message.from_user.id)
    if not user_db:
        await message.answer("Iltimos, avval ro'yxatdan o'ting (/register).")
        return

    await message.answer("Iltimos, sarf qilgan summangizni kiriting:")
    await message.answer("Masalan: 10 000 yoki 5000")
    await state.set_state(ExpenseStates.amount)

@router.message(ExpenseStates.amount)
async def process_expense_amount(message: Message, state: FSMContext):
    """
    Process the user's expense amount input.
    """
    try:
        amount = int(message.text.replace(" ", "").strip())
        if amount <= 0:
            raise ValueError("Sarf miqdori musbat bo'lishi kerak.")

        await state.update_data(amount=amount)
        await message.answer(f"Siz {amount} so'm sarf qildingiz. Iltimos, sarf sababini kiriting:")
        await state.set_state(ExpenseStates.description)

    except ValueError as e:
        await message.answer(f"Xato: {str(e)}. Iltimos, to'g'ri summani kiriting.")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}. Iltimos, qayta urinib ko'ring.")

@router.message(ExpenseStates.description)
async def process_expense_description(message: Message, state: FSMContext):
    """
    Process the user's expense description input.
    """
    description = message.text.strip()

    if not description:
        await message.answer("Iltimos, sarf sababini kiriting.")
        return
    await state.update_data(description=description)

    expense_data = await state.get_data()

    db = await anext(get_db())
    user_db = await get_user_by_tg_id(db, message.from_user.id)

    expense_db = await create_expense(db, user_id=user_db.id, **expense_data)
    if not expense_db:
        await message.answer("Sarf ma'lumotlarini saqlashda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        return

    await message.answer(f"Sizning sarf ma'lumotingiz saqlandi: {expense_data['amount']} so'm, Sababi: {description}")

    await state.clear()