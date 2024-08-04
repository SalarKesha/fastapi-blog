import os
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from config import BASE_DIR
from events import handle_db_event
from routers import user, post


app = FastAPI()
app.include_router(router=user.router, tags=['user'])
app.include_router(router=post.router, tags=['post'])
static_path = os.path.join(BASE_DIR, 'static', 'posts')
os.makedirs(static_path, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
handle_db_event(app)
