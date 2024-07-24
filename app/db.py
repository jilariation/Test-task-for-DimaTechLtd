from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base = declarative_base()


@asynccontextmanager
async def get_db():
    """
    Асинхронный контекстный менеджер для управления сеансом базы данных.

    Создает и предоставляет асинхронный сеанс SQLAlchemy для выполнения операций с базой данных. Обеспечивает
    корректное закрытие сеанса после завершения работы.

    Используется в функциях для работы с базой данных, обеспечивая автоматическое управление жизненным циклом
    сеанса.

    Возвращает:
    - session: Асинхронный сеанс SQLAlchemy для работы с базой данных.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
