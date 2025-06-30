from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class UserIn(BaseModel):
    """
    User input model for creating a new user.
    """
    name: str = Field(..., max_length=100, description="Name of the user")
    phone_number: str = Field(..., max_length=13, description="Phone number of the user")
    tg_id: int = Field(..., description="Telegram ID of the user")

class UserOut(BaseModel):
    """
    User output model for returning user information.
    """
    id: int = Field(..., description="Unique identifier of the user")
    name: str = Field(..., max_length=100, description="Name of the user")
    phone_number: str = Field(..., max_length=13, description="Phone number of the user")
    tg_id: int = Field(..., description="Telegram ID of the user")

    expenses: Optional[List["ExpenseOut"]] = Field(
        default_factory=list,
        description="List of expenses associated with the user"
    )

    model_config = ConfigDict(from_attributes=True)

    @property
    def sum_expenses(self) -> int:
        """
        Returns the total sum of all active expenses (is_active=True).
        """
        return sum(exp.amount for exp in (self.expenses or []) if getattr(exp, "is_active", False))


class ExpenseOut(BaseModel):
    """
    Expense output model for returning expense information.
    """
    description: str = Field(..., max_length=255, description="Description of the expense")
    amount: int = Field(..., description="Amount of the expense")
    is_active: bool = Field(default=True, description="Whether the expense is active")

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    def __repr__(self):
        return self.amount