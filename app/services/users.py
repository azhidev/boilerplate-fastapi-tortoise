from typing import List
from app.models import User
from app.schemas import UserCreate, UserRead
from app.schemas import BaseService


class UserService(BaseService[User, UserCreate]):
    def __init__(self):
        super().__init__(User)
    

    async def get_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        return await self.get_all(skip, limit)

    async def get_user_count(self) -> int:
        return await self.count()