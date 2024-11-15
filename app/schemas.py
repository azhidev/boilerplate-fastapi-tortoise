from pydantic import BaseModel
from app.models import User
from typing import Type, TypeVar, List, Generic, Optional
from tortoise import Model
from app.utils.jwt_auth import pwd_context
from fastapi import HTTPException, status
import base64, random, time, ulid
from tortoise.exceptions import IntegrityError  # Use this if using Tortoise ORM
from datetime import datetime


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: str
    username: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    redirect: Optional[str] = None


T = TypeVar("T", bound=Model)
C = TypeVar("C", bound=BaseModel)

# def generate_sortable_id() -> str:
#     # Get current timestamp in milliseconds
#     timestamp = int(time.time() * 1000)

#     # Generate a short random component to ensure uniqueness
#     random_part = random.randint(0, 9999)

#     # Combine timestamp and random part
#     raw_id = (timestamp << 16) | random_part  # Shift timestamp to make space for randomness

#     # Encode to base62 for compactness
#     encoded_id = base64.urlsafe_b64encode(raw_id.to_bytes((raw_id.bit_length() + 7) // 8, 'big')).decode('utf-8').rstrip('=')
#     return encoded_id


class BaseService(Generic[T, C]):
    model: Type[T]

    def __init__(self, model: Type[T]):
        self.model = model

    @staticmethod
    def generate_ulid():
        """Generate a sortable ULID."""
        return str(ulid.new())

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash the password using bcrypt."""
        return pwd_context.hash(password)

    async def create(self, create_data: C) -> T:
        """Create a new instance with password hashing, error handling, and unique constraint handling."""
        try:
            custom_id = self.generate_ulid()
            create_dict = create_data.model_dump()

            # Check if the 'password' field exists and hash it
            if "password" in create_dict:
                create_dict["password"] = self.hash_password(create_dict["password"])

            create_dict["id"] = custom_id  # Add generated ID to the data
            return await self.model.create(**create_dict)

        except IntegrityError as e:
            # This block handles unique constraint violations
            # Adjust the error handling depending on the database or ORM you’re using
            if "UNIQUE constraint failed" in str(e):  # Tortoise ORM error message pattern
                duplicate_field = str(e).split(".")[-1]  # Extract the field name from the error message
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Duplicate value for field '{duplicate_field}'")
            elif "duplicate key value violates unique constraint" in str(e):  # PostgreSQL error pattern
                duplicate_field = str(e).split("(")[1].split(")")[0]  # Extract the field name from the error message
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Duplicate value for field '{duplicate_field}'")
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate value for a unique field")

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating user: {str(e)}")

    async def get(self, object_id: int) -> T:
        return await self.model.get(id=object_id)

    async def update(self, object_id: int, update_data: C) -> T:
        obj = await self.get(object_id)
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        await obj.save()
        return obj

    async def delete(self, object_id: int):
        obj = await self.get(object_id)
        await obj.delete()

    async def get_all(self, skip: int = 0, limit: int = 10) -> List[T]:
        return await self.model.all().offset(skip).limit(limit).order_by("-id")

    async def count(self) -> int:
        return await self.model.all().count()


class ResponseModel(BaseModel):
    data: List[dict]
    total_data: int
    total_pages: int
    current_page: int
    per_page: int
    has_more: bool