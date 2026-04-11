from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from app.db.session import engine
from app.db import base 


from app.api.routes.auth import router as auth_router
from app.api.routes.expense import router as expense_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield



app = FastAPI(lifespan=lifespan)


# Routers (to be added)
app.include_router(auth_router)
app.include_router(expense_router)