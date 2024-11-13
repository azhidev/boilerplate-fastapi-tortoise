from fastapi import APIRouter, HTTPException, Query
from app.models import User
from app.schemas import UserCreate, UserRead, ResponseModel
from app.services import UserService
import math
router = APIRouter(
    prefix="/users",
    tags=["USER"],
    responses={404: {"description": "Not found"}},
)

user_service = UserService()

@router.post("", response_model=UserRead)
async def create_user_endpoint(user_data: UserCreate):
    return await user_service.create(user_data)

@router.get("/{user_id}", response_model=UserRead)
async def get_user_endpoint(user_id: str):  
    user = await user_service.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead)
async def update_user_endpoint(user_id: str, user_data: UserCreate):
    return await user_service.update(user_id, user_data)

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: str):
    await user_service.delete(user_id)
    return {"message": "User deleted"}

@router.get("", response_model=ResponseModel)
async def get_users_endpoint(page: int = Query(1), per_page: int = Query(10)):
    skip = (page - 1) * per_page
    limit = per_page
    
    fields = ['id', 'username']
    # Fetching users directly as ORM instances
    users = await user_service.get_users(skip, limit)
    total_users = await user_service.get_user_count()
    
    total_pages = math.ceil(total_users / per_page)
    has_more = page < total_pages
    serialized_user = []
    for user in users:
        user_dict = {field: getattr(user, field) for field in fields} if fields else user.__dict__
        serialized_user.append(user_dict)

        
    return ResponseModel(
        data=serialized_user,  # Directly return ORM instances
        total_data=total_users,
        total_pages=total_pages,
        current_page=page,
        per_page=per_page,
        has_more=has_more
    )