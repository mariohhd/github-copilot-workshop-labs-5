from passlib.context import CryptContext
from typing import Optional, Dict, List
from .auth import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User:
    users: List["User"] = []
    _id_counter = 1

    def __init__(self, id: int, username: str, email: str, hashed_password: str, full_name: Optional[str] = None):
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.is_active = True

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active
        }

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @classmethod
    def create_user(cls, user_data: UserCreate):
        if any(u.username == user_data.username for u in cls.users):
            raise ValueError("Username already exists")
        if any(u.email == user_data.email for u in cls.users):
            raise ValueError("Email already exists")
        hashed_password = cls.get_password_hash(user_data.password)
        user = User(cls._id_counter, user_data.username, user_data.email, hashed_password, user_data.full_name)
        cls.users.append(user)
        cls._id_counter += 1
        return user

    @classmethod
    def authenticate_user(cls, username: str, password: str) -> Optional["User"]:
        user = next((u for u in cls.users if u.username == username or u.email == username), None)
        if user and cls.verify_password(password, user.hashed_password):
            return user
        return None
