from typing import List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import User, WaitingList, Expense


####################### User Functions ######################
async def get_all_users(db: AsyncSession) -> list[User]:
    """
    Retrieve all users from the database.

    Args:
        db (AsyncSession): The database session to use for the query.
    Returns:
        list[User]: List of User objects.
    """
    result = await db.execute(select(User).options(selectinload(User.expenses)))
    return result.scalars().all()


async def get_user_by_tg_id(db: AsyncSession, tg_id: int) -> User | None:
    """
    Retrieve a user from the database by their Telegram ID.

    Args:
        db (AsyncSession): The database session to use for the query.
        tg_id (int): Telegram ID of the user.

    Returns:
        User | None: User object if found, None otherwise.
    """
    result = await db.execute(
        select(User).where(User.tg_id == tg_id)
    )
    return result.scalar_one_or_none()

async def get_user_by_phone_number(db: AsyncSession, phone_number: str) -> User | None:
    """
    Retrieve a user from the database by their phone number.

    Args:
        db (AsyncSession): The database session to use for the query.
        phone_number (str): Phone number of the user.

    Returns:
        User | None: User object if found, None otherwise.
    """
    result = await db.execute(
        select(User).where(User.phone_number == phone_number)
    )
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, tg_id: int, name: str, phone_number: str) -> User:
    """
    Set user information in the database.

    Args:
        db (AsyncSession): The database session to use for the operation.
        tg_id (int): Telegram ID of the user.
        name (str): Name of the user.
        phone_number (str): Phone number of the user.

    Returns:
        User: The created or updated User object.
    """
    user_db = await get_user_by_phone_number(db, phone_number)

    if not user_db:
        user = User(tg_id=tg_id, name=name, phone_number=phone_number)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    return user_db


####################### Expense Functions ######################
async def create_expense(db: AsyncSession, user_id: int, description: str, amount: int) -> Expense:
    """
    Create a new expense record in the database.

    Args:
        db (AsyncSession): The database session to use for the operation.
        user_id (int): ID of the user who made the expense.
        description (str): Description of the expense.
        amount (int): Amount of the expense.

    Returns:
        Expense: The created Expense object.
    """
    expense = Expense(user_id=user_id, description=description, amount=amount)
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense


async def get_expenses(db: AsyncSession) -> List[Expense]:
    """
    Retrieve all active (is_active=True) expenses from the database,
    including the related user object for each expense.

    Args:
        db (AsyncSession): The database session to use for the query.

    Returns:
        List[Expense]: List of active Expense objects with user loaded.
    """
    result = await db.execute(
        select(Expense)
        .where(Expense.is_active.is_(True))
        .options(selectinload(Expense.user))
        .order_by(Expense.created_at.desc())
    )
    return result.scalars().all()

async def clear_active_expenses(db: AsyncSession) -> int:
    """
    Deactivate (set is_active=False) all active expenses in the database.

    Args:
        db (AsyncSession): The database session to use for the operation.

    Returns:
        int: Number of rows updated.
    """
    result = await db.execute(
        update(Expense)
        .where(Expense.is_active.is_(True))
        .values(is_active=False)
    )
    await db.commit()
    return result.rowcount


###################### Waiting List Functions ######################
async def get_phone_number_from_waiting_list(db: AsyncSession, phone_number: str) -> str | None:
    """
    Retrieve the phone number from the waiting list for a given Telegram ID.

    Args:
        db (AsyncSession): The database session to use for the query.
        phone_number (str): Phone number to search for.

    Returns:
        str | None: Phone number if found, None otherwise.
    """
    result = await db.execute(
        select(WaitingList.phone_number).where(WaitingList.phone_number == phone_number)
    )
    return result.scalar_one_or_none()

async def add_to_waiting_list(db: AsyncSession, phone_number: str) -> WaitingList:
    """
    Add a phone number to the waiting list.

    Args:
        db (AsyncSession): The database session to use for the operation.
        phone_number (str): Phone number to add to the waiting list.

    Returns:
        WaitingList: The created WaitingList object.
    """
    if await get_phone_number_from_waiting_list(db, phone_number):
        raise ValueError("This phone number is already in the waiting list.")
    if len(phone_number) != 13:
        raise ValueError("Phone number must be 13 characters long.")

    waiting_list_entry = WaitingList(phone_number=phone_number)
    db.add(waiting_list_entry)
    await db.commit()
    await db.refresh(waiting_list_entry)
    return waiting_list_entry


######################## Additional Functions (if needed) ######################
async def get_option_amounts_from_user_history_expanses(db: AsyncSession, tg_id: int):
    """
    Retrieve the amounts of options from user history expenses.

    This function is a placeholder and should be implemented based on your application's requirements.
    """
    user_db = await get_user_by_tg_id(db, tg_id)
    if user_db:
        expenses = await db.execute(
            select(Expense.amount).where(Expense.user_id == user_db.id, Expense.is_active.is_(True)).limit(6)
        )
        return expenses.scalars().all()
