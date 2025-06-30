from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database import get_db
from schema import UserIn
from service import get_user_by_tg_id, create_user, get_phone_number_from_waiting_list
from states import Register
import keyboards as kb


router = Router()

@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    """
    Handle the /register command to start user registration.
    """
    db = await anext(get_db())

    user_db = await get_user_by_tg_id(db, message.from_user.id)

    if user_db:
        await message.answer("Siz allaqachon ro'yxatdan o'tgansiz.")
        return

    await state.set_state(Register.name)
    await message.answer("Iltimos, ismingizni kiriting:")

@router.message(Register.name)
async def process_name(message: Message, state: FSMContext):
    """
    Process the user's name input during registration.
    """
    await state.update_data(name=message.text)
    await state.set_state(Register.phone_number)
    await message.answer("Iltimos, telefon raqamingizni kiriting:", reply_markup=kb.get_number)

@router.message(Register.phone_number, F.contact)
async def process_phone_number(message: Message, state: FSMContext):
    """
    Process the user's phone number input during registration.
    """
    if not message.contact or not message.contact.phone_number:
        await message.answer("Iltimos, telefon raqamingizni yuboring.")
        return

    await state.update_data(phone_number=message.contact.phone_number)

    user_data = await state.get_data()
    user_data['tg_id'] = message.from_user.id

    db = await anext(get_db())

    user_validation = UserIn.model_validate(user_data)
    if not user_validation:
        await message.answer("Iltimos, ma'lumotlaringizni to'g'ri kiriting.")
        return

    waiting_list_validation = await get_phone_number_from_waiting_list(db, user_data['phone_number'])
    if waiting_list_validation:
        await message.answer("Sizning telefon raqamingiz kutish ro'yxatida mavjud emas. Iltimos, admin bilan bog'laning.")
        return

    user_db = await create_user(db, **user_data)

    if user_db:
        await message.answer(f"Ro'yxatdan o'tish muvaffaqiyatli yakunlandi! Xush kelibsiz, {user_db.name}!",
                             reply_markup=kb.user_kb)
    else:
        await message.answer("Ro'yxatdan o'tishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.",
                             reply_markup=None)
    await state.clear()