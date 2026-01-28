from fastapi import APIRouter, HTTPException
from database.rds_client import RDSClient
from utils.logger import app_logger
from models.schemas import UserCreate

router = APIRouter(prefix="/users")
db = RDSClient()

@router.get("/")
async def list_users():
    app_logger.info("Fetching all users")
    return db.get_all_users()

@router.get("/{user_id}")
async def user_details(user_id: int):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/create")
async def add_user(user: UserCreate):
    app_logger.info(f"Creating new user: {user.email}")
    new_id = db.create_user(user.model_dump())
    return {"message": "User created successfully", "user_id": new_id}