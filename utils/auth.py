from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from database import db
from fastapi import HTTPException, Depends, status
from passlib.context import CryptContext
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from datetime import datetime, timezone, timedelta
import jwt
from schemas.user import UserCreateSchema, UserDbSchema, UserSchema
from bson import ObjectId

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user(username) -> dict:
    return await db.users.find_one({'username': username})


async def authenticate_user(username, password):
    user = await get_user(username)
    if not user:
        return False
    if not pwd_context.verify(password, user['password']):
        return False
    return user


def create_access_token(username):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        'sub': username,
        'exp': expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema:
    credential_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Unauthorized error')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get('sub')
        if not username:
            raise credential_exception
    except InvalidTokenError:
        raise credential_exception
    user = await get_user(username)
    if not user:
        raise HTTPException
    return UserSchema(user_id=user['user_id'], username=user['username'])
