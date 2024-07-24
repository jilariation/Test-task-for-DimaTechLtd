from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.user import User


async def register_user(session: AsyncSession, email: str, full_name: str, password: str) -> (User, str):
    """
    Регистрация нового пользователя.

    Создает новый объект пользователя с предоставленным `email`, `full_name` и `password`. Затем добавляет его в базу данных.
    Если пользователь с таким email уже существует, возвращает сообщение об ошибке.

    Аргументы:
    - session: SQLAlchemy AsyncSession для взаимодействия с базой данных.
    - email: Email нового пользователя.
    - full_name: Полное имя нового пользователя.
    - password: Пароль нового пользователя.

    Возвращает:
    - user: Созданный объект пользователя (или None, если произошла ошибка).
    - str: Сообщение об ошибке (или None, если регистрация прошла успешно).
    """
    user = User(email=email, full_name=full_name)
    user.set_password(password)
    session.add(user)
    try:
        await session.commit()
        return user, None
    except IntegrityError:
        await session.rollback()
        return None, 'User with this email already exists'


async def login_user(session: AsyncSession, email: str, password: str) -> (User, bool):
    """
    Аутентификация пользователя.

    Находит пользователя по `email` и проверяет его пароль. Возвращает объект пользователя и флаг успешной аутентификации.

    Аргументы:
    - session: SQLAlchemy AsyncSession для взаимодействия с базой данных.
    - email: Email пользователя для аутентификации.
    - password: Пароль пользователя для проверки.

    Возвращает:
    - user: Объект пользователя (или None, если аутентификация не удалась).
    - bool: Флаг успешной аутентификации (True, если пароль верен; False в противном случае).
    """
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if user and user.verify_password(password):
        return user, True
    return None, False
