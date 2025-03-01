from fastapi import APIRouter, Depends, HTTPException
from models import User
from database import users_collection
from auth import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/signup")
async def signup(user: User):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    new_user = {"username": user.username, "email": user.email, "password": hashed_password}
    await users_collection.insert_one(new_user)
    return {"message": "User created successfully"}

@router.post("/login")
async def login(user: User):
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user["email"]}, timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}
