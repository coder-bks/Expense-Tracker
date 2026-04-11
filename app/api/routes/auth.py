from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, Login
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])



@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check existing user (email or username)
    statement = select(User).where(
        (User.email == user.email) | (User.username == user.username)
    )
    existing_user = db.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    # Hash password
    hashed_password = hash_password(user.password)

    # Create user
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login")
def login(user: Login, db: Session = Depends(get_db)):
    # Fetch user by email
    statement = select(User).where(User.email == user.email)
    db_user = db.exec(statement).first()

    # Validate user + password
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create JWT token
    token = create_access_token(data={"sub": str(db_user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }