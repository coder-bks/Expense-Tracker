from fastapi import APIRouter, Depends, Response
from sqlmodel import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseRead
from app.core.jwt import get_current_user

from app.crud.expense import (
    create_expense,
    get_expenses,
    update_expense,
    delete_expense,
)


router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=ExpenseRead, status_code=201)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_expense(db, expense, current_user.id)


@router.get("/", response_model=list[ExpenseRead])
def list_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_expenses(db, current_user.id)


@router.put("/{id}", response_model=ExpenseRead)
def edit_expense(
    id: int,
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_expense(db, id, expense, current_user.id)


@router.delete("/{id}")
def remove_expense(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_expense(db, id, current_user.id)
    return Response(status_code=204)