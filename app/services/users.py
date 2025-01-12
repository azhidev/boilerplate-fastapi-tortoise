from typing import List
from app.models import User
from app.schemas import UserCreate, UserLogin
from app.schemas import BaseService
import jwt
from tortoise.exceptions import DoesNotExist  # Import DoesNotExist for handling missing records

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from typing import List
from dotenv import load_dotenv
import os
from app.utils.jwt_auth import pwd_context

load_dotenv()
# Password hashing setup

# Your secret key for JWT generation
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_EXPIRE_TIME = os.getenv("JWT_EXPIRE_TIME")
ALGORITHM = "HS256"


class UserService(BaseService[User, UserCreate]):
    def __init__(self):
        super().__init__(User)

    async def get_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        return await self.get_all(skip, limit)

    async def get_user_count(self) -> int:
        return await self.count()

    async def authenticate(self, user_data: UserLogin) -> dict:
        try:
            # Fetch user from DB by username
            user = await self.model.get(username=user_data.username)

        except DoesNotExist:
            # Raise HTTP 404 if the user is not found
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Check if the provided password matches the stored hashed password
        if not self.verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        # Generate and return a JWT token
        token = self.create_jwt_token(user_data)
        return {"access_token": token, "token_type": "bearer"}

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify that the provided password matches the stored hashed password."""
        return pwd_context.verify(plain_password, hashed_password)

    def create_jwt_token(self, user_data: User) -> str:
        """Generate a JWT token for the user."""
        expiration = datetime.now(timezone.utc) + timedelta(seconds=int(JWT_EXPIRE_TIME))  # Set token expiration (1 hour)
        token_data = {"username": user_data.username, "exp": expiration}
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return token
