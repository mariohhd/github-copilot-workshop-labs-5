from fastapi import APIRouter, HTTPException, status
from app.models.user import User
from app.models.auth import UserCreate, UserLogin, Token
from app.utils.jwt import create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate):
    try:
        user = User.create_user(user_data)
        return user.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
def login(login_data: UserLogin):
    user = User.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")
