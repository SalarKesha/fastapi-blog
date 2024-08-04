from bson import ObjectId
from fastapi import HTTPException, status
from config import BASE_DIR
import random


def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid object id')


def make_random_str(length=12):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))


def generate_random_file_name(file_name: str):
    name = file_name.split('.')[0]
    extension = file_name.split('.')[-1]
    return name + make_random_str() + '.' + extension

