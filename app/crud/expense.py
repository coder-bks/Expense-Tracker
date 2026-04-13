from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate


def create_expense(db: Session, expense: ExpenseCreate, user_id: int) -> Expense:
    db_expense = Expense(
        title=expense.title,
        amount=expense.amount,
        user_id=user_id,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses(db: Session, user_id: int) -> list[Expense]:
    statement = select(Expense).where(Expense.user_id == user_id)
    return list(db.exec(statement).all())


def update_expense(
    db: Session,
    expense_id: int,
    expense: ExpenseCreate,
    user_id: int,
) -> Expense:
    db_expense = db.get(Expense, expense_id)

    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    if db_expense.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    db_expense.title = expense.title
    db_expense.amount = expense.amount

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def delete_expense(db: Session, expense_id: int, user_id: int) -> None:
    db_expense = db.get(Expense, expense_id)

    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    if db_expense.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    db.delete(db_expense)
    db.commit()