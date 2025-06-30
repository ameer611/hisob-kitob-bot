from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import keyboards as kb
from database import get_db
from states import WaitingListStates, MessageStates
from service import get_user_by_tg_id, create_expense, get_all_users, clear_active_expenses, get_expenses, \
    add_to_waiting_list
from settings import settings

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Handle the /start command.
    """
    db = await anext(get_db())

    user_db = await get_user_by_tg_id(db, message.from_user.id)

    await message.answer("Assalomu alaykum, bu bot bizning o'zaro hisob-kitoblarimizni osonlashtirish uchun yasaldi.")
    await message.answer("Botga xush kelibsiz!")
    return_message = {}

    if user_db and user_db.tg_id in settings.admin_users_ids:
        return_message['text'] = f"Assalomu alaykum, admin {user_db.name}!"
        return_message['reply_markup'] = kb.admin_kb
    elif user_db:
        return_message['text'] = f"Assalomu alaykum, {user_db.name}!"
        return_message['reply_markup'] = kb.user_kb

    if not return_message:
        return_message['text'] = "Assalomu alaykum! Botdan foydalanish uchun ro'yxatdan o'ting(/register)."
        return_message['reply_markup'] = None

    await message.answer(**return_message)

@router.message(F.text == "Taklif qilish 📨")
async def handle_suggestion(message: Message, state: FSMContext):
    """
    Handle the user's suggestion input.
    """
    if not message.from_user.id:
        await message.answer("Iltimos, avval ro'yxatdan o'ting (/register).")
        return

    if not message.from_user.id in settings.admin_users_ids:
        await message.answer("Siz taklif qila olmaysiz, faqat adminlar taklif qila oladi.")
        return

    await state.set_state(WaitingListStates.phone_number)
    await message.answer("Iltimos, taklif qilmoqchi bo'lgan foydalanuvchining telefon raqamini yuboring:")

@router.message(WaitingListStates.phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    """
    Process the user's phone number input for suggestions.
    """
    await state.update_data(phone_number=message.text.strip())

    data = await state.get_data()

    db = await anext(get_db())
    user_db = await add_to_waiting_list(db, data['phone_number'])
    if not user_db:
        await message.answer("Taklif yuborishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        return
    await message.answer(f"Taklif yuborildi! Sizning taklifingiz: {data['phone_number']}")

    await state.clear()

@router.message(F.text == "Xabar yuborish 📲")
async def handle_message(message: Message, state: FSMContext):
    """
    Handle the user's message input.
    """
    if not message.from_user.id:
        await message.answer("Iltimos, avval ro'yxatdan o'ting (/register).")
        return

    if not message.from_user.id in settings.admin_users_ids:
        await message.answer("Siz xabar yubora olmaysiz, faqat adminlar xabar yubora oladi.")
        return

    await state.set_state(MessageStates.text)
    await message.answer("Iltimos, yubormoqchi bo'lgan xabaringizni kiriting:")

@router.message(MessageStates.text)
async def process_message_text(message: Message, state: FSMContext, bot: Bot):
    """
    Process the user's message input.
    """
    if not message.text:
        await message.answer("Iltimos, xabar matnini kiriting.")
        return

    data = await state.get_data()

    db = await anext(get_db())
    users_db = await get_all_users(db)

    if not users_db:
        await message.answer("Siz ro'yxatdan o'tmagan foydalanuvchisiz. Iltimos, avval ro'yxatdan o'ting (/register).")
        return

    success, failure = 0, 0
    for user in users_db:
        if user.tg_id != message.from_user.id:
            try:
                await bot.send_message(user.tg_id, message.text)
                success += 1
            except Exception as e:
                failure += 1

    await message.answer(
        f"Sizning xabaringiz {success} foydalanuvchiga yuborildi."
        + (f"\nYuborib bo'lmadi: {failure} foydalanuvchi." if failure else "")
    )
    await state.clear()






