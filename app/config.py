import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/mydatabase")
SECRET_KEY = os.getenv("SECRET_KEY", "gfdmhghif38yrf9ew0jkf32")
SECRET_JWT_KEY = os.getenv("SECRET_JWT_KEY", "dbcff2054d1d0b6ff0d28370d777e8c737e3646b3eeb4d51")
