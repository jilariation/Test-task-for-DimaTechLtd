from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.models.user import User


async def create_user(session: AsyncSession, email: str, full_name: str, password: str) -> User:
    """
    Создание нового пользователя.

    Создает объект пользователя с заданными `email`, `full_name` и `password`. Затем добавляет его в сессию и сохраняет в базе данных.

    Аргументы:
    - session: SQLAlchemy AsyncSession для взаимодействия с базой данных.
    - email: Email нового пользователя.
    - full_name: Полное имя нового пользователя.
    - password: Пароль нового пользователя.

    Возвращает:
    - Созданный объект пользователя.
    """
    user = User(email=email, full_name=full_name)
    user.set_password(password)
    session.add(user)
    await session.commit()
    return user


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    """
    Удаление пользователя по идентификатору.

    Находит пользователя по `user_id` и удаляет его из базы данных, если он существует.

    Аргументы:
    - session: SQLAlchemy AsyncSession для взаимодействия с базой данных.
    - user_id: Идентификатор пользователя, которого нужно удалить.

    Возвращает:
    - True, если пользователь был найден и успешно удален.
    - False, если пользователь не найден.
    """
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user:
        await session.delete(user)
        await session.commit()
        return True
    return False


async def update_user(session: AsyncSession, user_id: int, email: str = None, full_name: str = None,
                      password: str = None) -> bool:
    """
    Обновление информации о пользователе.

    Находит пользователя по `user_id` и обновляет его данные, если они предоставлены. Сохраняет изменения в базе данных.

    Аргументы:
    - session: SQLAlchemy AsyncSession для взаимодействия с базой данных.
    - user_id: Идентификатор пользователя, информацию о котором нужно обновить.
    - email: Новый email пользователя (или None, если не обновляется).
    - full_name: Новое полное имя пользователя (или None, если не обновляется).
    - password: Новый пароль пользователя (или None, если не обновляется).

    Возвращает:
    - True, если пользователь был найден и обновлен.
    - False, если пользователь не найден.
    """
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user:
        if email:
            user.email = email
        if full_name:
            user.full_name = full_name
        if password:
            user.set_password(password)
        await session.commit()
        return True
    return False


async def get_users(session: AsyncSession):
    """
    Получение списка всех пользователей.

    Извлекает всех пользователей из базы данных, включая их счета, и возвращает список уникальных пользователей.

    Аргументы:
    - session: SQLAlchemy AsyncSession для взаимодействия с базой данных.

    Возвращает:
    - Список объектов пользователей, извлеченных из базы данных.
    """
    result = await session.execute(
        select(User).options(joinedload(User.accounts)).distinct()
    )
    users = result.scalars().unique().all()
    return users
