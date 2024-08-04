# FastAPI Blog

config.py file:
```python
from pathlib import Path
MONGO_HOST = ''
MONGO_DATABASE = ''
MONGO_PORT = 27017
MONGO_USER = ''
MONGO_PASSWORD = ''
SECRET_KEY = ''
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
BASE_DIR = Path(__file__).resolve().parent
```