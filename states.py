from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    """
    State group for user registration.
    """
    name = State()
    phone_number = State()


class ExpenseStates(StatesGroup):
    """
    State group for handling user expenses.
    """
    amount = State()
    description = State()

class WaitingListStates(StatesGroup):
    """
    State group for handling waiting list registration.
    """
    phone_number = State()

class MessageStates(StatesGroup):
    """
    State group for handling messages.
    """
    text = State()