from typing import Any, Sequence

from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.account import Account
from app.models.payments import Payment
from app.models.user import User


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    """
    Получение пользователя по его идентификатору.

    Выполняет запрос к базе данных для получения пользователя по предоставленному `user_id`.

    Аргументы:
    - session: SQLAlchemy AsyncSession для взаимодействия с базой данных.
    - user_id: Идентификатор пользователя.

    Возвращает:
    - User: Объект пользователя (или None, если пользователь не найден).
    """
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def get_accounts_by_user_id(session: AsyncSession, user_id: int) -> Sequence[Row[Any] | RowMapping | Any]:
    """
    Получение счетов пользователя по его идентификатору.

    Выполняет запрос к базе данных для получения всех счетов пользователя по предоставленному `user_id`.

    Аргументы:
    - session: SQLAlchemy AsyncSession для взаимодействия с базой данных.
    - user_id: Идентификатор пользователя.

    Возвращает:
    - Sequence[Row[Any] | RowMapping | Any]: Список объектов счетов пользователя (или пустой список, если счета не найдены).
    """
    result = await session.execute(select(Account).where(Account.owner_id == user_id))
    return result.scalars().all()


async def get_payments_by_user_id(session: AsyncSession, user_id: int) -> Sequence[Row[Any] | RowMapping | Any]:
    """
    Получение платежей пользователя по его идентификатору.

    Выполняет запрос к базе данных для получения всех платежей пользователя по предоставленному `user_id`,
    включая данные связанных счетов.

    Аргументы:
    - session: SQLAlchemy AsyncSession для взаимодействия с базой данных.
    - user_id: Идентификатор пользователя.

    Возвращает:
    - Sequence[Row[Any] | RowMapping | Any]: Список объектов платежей пользователя (или пустой список, если платежи не найдены).
    """
    result = await session.execute(select(Payment).join(Account).where(Account.owner_id == user_id))
    return result.scalars().all()
