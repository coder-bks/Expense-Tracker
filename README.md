# Expense Tracker API
 
A RESTful API for tracking personal expenses, built with FastAPI and PostgreSQL. Focuses on production-like backend architecture with JWT authentication and user-scoped data isolation.
 
---
 
## Features
 
- JWT-based authentication (register, login)
- Password hashing with bcrypt
- Full CRUD for expenses
- User-scoped data — users can only access their own expenses
- Auto-generated Swagger docs at `/docs`
- Deployed on Railway
---
 
## Tech Stack
 
| Tool | Purpose |
|---|---|
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLModel | ORM — database models and queries |
| Passlib (bcrypt) | Password hashing |
| python-jose | JWT token creation and verification |
| pydantic-settings | Environment variable management |
| pytest + httpx | Testing |
 
---
 
## Project Structure
 
```
expense-tracker/
├── app/
│   ├── main.py               # App entry point
│   ├── core/
│   │   ├── config.py         # Environment variables
│   │   ├── security.py       # Password hashing
│   │   └── jwt.py            # Token creation and verification
│   ├── db/
│   │   ├── session.py        # Database engine and session
│   │   └── base.py           # Model registration
│   ├── models/
│   │   ├── user.py           # User table
│   │   └── expense.py        # Expense table
│   ├── schemas/
│   │   ├── user.py           # User request/response schemas
│   │   └── expense.py        # Expense request/response schemas
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py       # Register and login endpoints
│   │       └── expense.py    # Expense CRUD endpoints
│   └── crud/
│       └── expense_crud.py   # Database logic layer
└── tests/
    └── test_auth.py          # Auth endpoint tests
```
 
---
 
## API Endpoints
 
### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Create a new account |
| POST | `/auth/login` | Login and receive JWT token |
 
### Expenses (Protected)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/expenses/` | Add a new expense |
| GET | `/expenses/` | Get all your expenses |
| PUT | `/expenses/{id}` | Update an expense |
| DELETE | `/expenses/{id}` | Delete an expense |
 
All expense endpoints require `Authorization: Bearer <token>` header.
 
---
 
## Running Locally
 
**1. Clone the repo:**
```bash
git clone https://github.com/coder-bks/expense-tracker.git
cd expense-tracker
```
 
**2. Create virtual environment and install dependencies:**
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
 
**3. Create a `.env` file at the project root:**
```
DATABASE_URL=postgresql://user:password@localhost:5432/expense_tracker
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
 
**4. Run the server:**
```bash
uvicorn app.main:app --reload
```
 
**5. Open Swagger UI:**
```
http://127.0.0.1:8000/docs
```
 
---
 

 
---
 
## Design Decisions
 
**Why FastAPI?** Auto-generated docs, Pydantic validation out of the box, and significantly faster than Flask for API workloads.
 
**Why SQLModel?** Combines SQLAlchemy and Pydantic — models double as schemas, reducing boilerplate without losing flexibility.
 
**Why separate schemas from models?** Models define what's stored in the database. Schemas define what the API accepts and returns. This separation ensures sensitive fields like `hashed_password` are never accidentally exposed in a response.
 
**403 vs 404 on ownership checks** — returning `404` on a forbidden resource leaks information about what exists. `403` is the correct response when the resource exists but doesn't belong to the requesting user.
 
---
 
## Author
 
**Balkrishna Sawant**  
Python Backend Developer  
[LinkedIn](https://linkedin.com/in/yourprofile)
 