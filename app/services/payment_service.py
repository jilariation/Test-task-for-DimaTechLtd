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


async def get_payment_by_transaction_id(session: AsyncSession, transaction_id: str) -> Payment:
    """
    Получение платежа по его идентификатору транзакции.

    Выполняет запрос к базе данных для получения платежа по предоставленному `transaction_id`.

    Аргументы:
    - session: SQLAlchemy AsyncSession для взаимодействия с базой данных.
    - transaction_id: Идентификатор транзакции.

    Возвращает:
    - Payment: Объект платежа (или None, если платеж не найден).
    """
    result = await session.execute(select(Payment).where(Payment.transaction_id == transaction_id))
    return result.scalars().first()


async def get_account_by_id_and_user_id(session: AsyncSession, account_id: int, user_id: int) -> Account:
    """
    Получение счета по его идентификатору и идентификатору пользователя.

    Выполняет запрос к базе данных для получения счета по предоставленным `account_id` и `user_id`.

    Аргументы:
    - session: SQLAlchemy AsyncSession для взаимодействия с базой данных.
    - account_id: Идентификатор счета.
    - user_id: Идентификатор пользователя.

    Возвращает:
    - Account: Объект счета (или None, если счет не найден).
    """
    result = await session.execute(
        select(Account).where(Account.id == account_id, Account.owner_id == user_id))
    return result.scalars().first()


async def create_account(session: AsyncSession, account_id: int, user_id: int) -> Account:
    """
    Создание нового счета.

    Создает новый объект счета с предоставленным `account_id` и `user_id`, устанавливает начальный баланс в 0,
    добавляет его в базу данных.

    Аргументы:
    - session: SQLAlchemy AsyncSession для взаимодействия с базой данных.
    - account_id: Идентификатор нового счета.
    - user_id: Идентификатор владельца счета.

    Возвращает:
    - Account: Созданный объект счета.
    """
    account = Account(id=account_id, balance=0, owner_id=user_id)
    session.add(account)
    await session.commit()
    return account


async def create_payment(session: AsyncSession, transaction_id: str, amount: float, account_id: int) -> Payment:
    """
    Создание нового платежа.

    Создает новый объект платежа с предоставленным `transaction_id`, `amount` и `account_id`, добавляет его в базу данных.

    Аргументы:
    - session: SQLAlchemy AsyncSession для взаимодействия с базой данных.
    - transaction_id: Идентификатор транзакции.
    - amount: Сумма платежа.
    - account_id: Идентификатор счета, на который поступает платеж.

    Возвращает:
    - Payment: Созданный объект платежа.
    """
    payment = Payment(transaction_id=transaction_id, amount=amount, account_id=account_id)
    session.add(payment)
    await session.commit()
    return payment


async def update_account_balance(session: AsyncSession, account: Account, amount: float) -> Account:
    """
    Обновление баланса счета.

    Увеличивает баланс предоставленного счета на заданную сумму и сохраняет изменения в базе данных.

    Аргументы:
    - session: SQLAlchemy AsyncSession для взаимодействия с базой данных.
    - account: Объект счета, баланс которого нужно обновить.
    - amount: Сумма, на которую нужно увеличить баланс.

    Возвращает:
    - Account: Обновленный объект счета.
    """
    account.balance += amount
    await session.commit()
    return account
