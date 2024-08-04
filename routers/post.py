from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from starlette import status
import os
from config import BASE_DIR
from database import db
from schemas.user import UserSchema
from utils.auth import get_current_user
from utils.tools import validate_object_id
from bson import ObjectId
from schemas.post import PostSchema, PostOutSchema, PostDbSchema
from utils.tools import generate_random_file_name
import aiofiles

router = APIRouter()


@router.get('/post/list', response_model=list[PostOutSchema], status_code=status.HTTP_200_OK)
async def get_posts():
    posts_cursor = db.posts.find()
    posts = await posts_cursor.to_list(length=100)
    return posts


@router.get('/post/{post_id}', response_model=PostOutSchema, status_code=status.HTTP_200_OK)
async def get_post(post_id: str):
    validate_object_id(post_id)
    post = await db.posts.find_one({'post_id': post_id})
    return post


@router.post('/post/create', status_code=status.HTTP_201_CREATED)
async def create_post(title: str = Form(...), content: str = Form(...), image: UploadFile = File(),
                      user: UserSchema = Depends(get_current_user)):
    file_name = generate_random_file_name(image.filename)
    file_path = os.path.join('static', 'posts', file_name)
    absolute_file_path = os.path.join(BASE_DIR, file_path)
    try:
        async with aiofiles.open(absolute_file_path, 'wb') as f:
            while chunked := await image.read(1024):
                await f.write(chunked)
        document_id = str(ObjectId())
        temp_post = PostDbSchema(post_id=document_id, author=user, title=title, content=content, image=file_path)
        new_post = await db.posts.insert_one(temp_post.model_dump())
        return {'post_id': document_id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
