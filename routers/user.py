from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.token import TokenSchema
from schemas.user import UserCreateSchema, UserDbSchema
from utils.auth import authenticate_user, create_access_token, get_current_user, pwd_context
from utils.auth import get_user
from database import db
from schemas.user import UserSchema
from bson import ObjectId

router = APIRouter()


@router.post('/token', response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    access_token = create_access_token(username=user['username'])
    return TokenSchema(access_token=access_token)


@router.get('/me', response_model=UserSchema, status_code=status.HTTP_200_OK)
async def get_user_info(user: UserSchema = Depends(get_current_user)):
    return user


@router.post('/user/create', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateSchema):
    temp_user = await get_user(user.username)
    if temp_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This username already exists')
    hashed_password = pwd_context.hash(user.password)
    document_id = str(ObjectId())
    try:
        await db.users.insert_one(UserDbSchema(
            user_id=document_id,
            username=user.username,
            password=hashed_password
        ).model_dump())
        return {'user_id': document_id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('/user/list', response_model=list[UserSchema], status_code=status.HTTP_200_OK)
async def get_users():
    users_cursor = db.users.find()
    users = await users_cursor.to_list(length=100)
    return users
