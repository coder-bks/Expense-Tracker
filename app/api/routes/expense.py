from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select

from app.db.session import get_db
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseRead
from app.core.jwt import get_current_user


router = APIRouter(prefix="/expenses", tags=["expenses"])


# POST /expenses — add expense
@router.post("/", response_model=ExpenseRead)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_expense = Expense(
        title=expense.title,
        amount=expense.amount,
        user_id=current_user.id
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense


# GET /expenses — get current user's expenses
@router.get("/", response_model=list[ExpenseRead])
def get_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = select(Expense).where(Expense.user_id == current_user.id)
    expenses = db.exec(statement).all()
    return expenses


# PUT /expenses/{id} — update expense
@router.put("/{id}", response_model=ExpenseRead)
def update_expense(
    id: int,
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_expense = db.get(Expense, id)

    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if db_expense.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    db_expense.title = expense.title
    db_expense.amount = expense.amount

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense


# DELETE /expenses/{id} — delete expense
@router.delete("/{id}")
def delete_expense(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_expense = db.get(Expense, id)

    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if db_expense.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    db.delete(db_expense)
    db.commit()

    return Response(status_code=204)