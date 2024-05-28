# from fastapi import APIRouter, HTTPException, Depends,status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from typing import List
# from ..auth import create_access_token
# from ..models import UserModel
# from ..schemas import UserCreateSchema, UserResponseSchema
# from ..crud import create_user, get_user_by_username

# router = APIRouter()
# oauth_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

# @router.post("/register",status_code=status.HTTP_201_CREATED)
# async def register(user: UserCreateSchema):
#     existing_user = await get_user_by_username(user.username)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     user_model = UserModel(
#         username=user.username,
#         email=user.email,
#         hashed_password=UserModel.hash_password(user.password),
#     )
#     created_user = await create_user(user_model)
#     access_token = create_access_token(data={"sub": created_user.username})
#     # print(created_user)
#     # return { "Message" : "User was created successfully!!" }  # Make sure this contains the `id` field
#     return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await get_user_by_username(form_data.username)
#     if not user or not user.verify_password(form_data.password):
#         raise HTTPException(
#             status_code=400,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}


from fastapi import APIRouter, HTTPException, Depends, Request,status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from auth import TokenData, create_access_token, create_refresh_token, get_current_user  # noqa: E402
from models import UserModel  # noqa: E402
from schemas import UserCreateSchema, UserResponseSchema,TokenSchema,TokenResponseSchema  # noqa: E402
from crud import create_user, get_user_by_username
from datetime import datetime, timedelta
from auth import SECRET_KEY, ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES  # noqa: E402


router = APIRouter()

REFRESH_TOKEN_EXPIRE_DAYS = 7

@router.post("/register",response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreateSchema, req:Request):
    print(await req.json())
    existing_user = await get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_model = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=UserModel.hash_password(user.password),
    )
    created_user = await create_user(user_model)
    return created_user

@router.post("/token", response_model=TokenResponseSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_username(form_data.username)
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": user.username})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponseSchema)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.post("/refresh-token", response_model=TokenSchema)
async def refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        token_data = TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await get_user_by_username(username=token_data.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    rt = create_refresh_token(data={"sub": user.username})

    return {"access_token": access_token, "refresh_token": rt, "token_type": "bearer"}