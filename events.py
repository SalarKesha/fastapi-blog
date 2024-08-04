from fastapi import FastAPI
from database import db


async def create_index():
    await db.users.create_index("user_id", unique=True, name='user_id_index')
    await db.posts.create_index("post_id", unique=True, name='post_id_index')


def handle_db_event(app: FastAPI):
    @app.on_event('startup')
    async def startup():
        print('================== Connecting to mongo ==================')
        print(await db.client.admin.command('ping'))
        await create_index()

    @app.on_event('shutdown')
    def shutdown():
        db.client.close()
        print('================== Mongo disconnected ==================')
