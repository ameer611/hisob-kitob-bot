from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from service import get_option_amounts_from_user_history_expanses

admin_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Pul sarf qildim💸")],
                                         [KeyboardButton(text="Hisobot🧾")],
                                         [KeyboardButton(text="Taklif qilish 📨"),
                                          KeyboardButton(text="Xabar yuborish 📲")]],
                            resize_keyboard=True,
                            input_field_placeholder="Admin menyusi...")

user_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Pul sarf qildim💸")],
                                        [KeyboardButton(text="Hisobot🧾")]],
                            resize_keyboard=True,
                            input_field_placeholder="Foydalanuvchi menyusi...")

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Telefon raqamini yuborish🤙", request_contact=True)]],
                                    resize_keyboard=True,
                                    input_field_placeholder="Telefon raqamini yuboring...")

calculated_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Hisob-kitob qilindi ✅", callback_data="calculated")]
])

# async def get_option_amounts(db: AsyncSession, tg_id: int) -> ReplyKeyboardMarkup:
#     """
#     Create a keyboard for selecting amounts.
#
#     Returns:
#         ReplyKeyboardMarkup: The keyboard with amount options.
#     """
#     amounts = await get_option_amounts_from_user_history_expanses(db, tg_id)
#     keyboard = InlineKeyboardBuilder()
#
#     if amounts:
#         for amount in amounts:
#             keyboard.add(InlineKeyboardButton(text=str(amount)))
#         return keyboard.as_markup(resize_keyboard=True, input_field_placeholder="Sarf qilingan summani tanlang yoki kiriting...")
#
#     return None  # Return None if no amounts are available
