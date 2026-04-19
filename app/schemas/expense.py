from datetime import datetime
from sqlmodel import SQLModel


class ExpenseCreate(SQLModel):
    title: str
    amount: float


class ExpenseRead(SQLModel):
    id: int
    user_id: int
    title: str
    amount: float
    created_at: datetime