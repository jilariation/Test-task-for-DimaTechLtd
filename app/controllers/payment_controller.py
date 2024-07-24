from sanic import response, Blueprint
from sanic.request import Request
from sqlalchemy.exc import IntegrityError

from app.db import get_db
from app.config import SECRET_KEY
from app.services import payment_service
from app.utils.signature import generate_signature

bp = Blueprint('payment')


@bp.post('/webhook/payment')
async def handle_webhook(request: Request):
    """
    Обработка вебхука платежной системы.

    Проверяет подпись данных вебхука на соответствие с ожидаемой подписью. Затем выполняет следующие действия:
    1. Проверяет, существует ли пользователь с указанным `user_id`. Если пользователь не найден, возвращает ошибку 404.
    2. Проверяет, существует ли уже платеж с указанным `transaction_id`. Если платеж уже обработан, возвращает ошибку 400.
    3. Проверяет, существует ли счет с указанным `account_id` для данного пользователя. Если счет не найден, создается новый.
    4. Создает новый платеж и обновляет баланс счета на указанную сумму. При возникновении ошибок во время транзакции откатывает изменения и возвращает ошибку 500.

    Аргументы:
    - request: Sanic Request объект, содержащий данные вебхука платежной системы.

    Возвращает:
    - JSON-ответ с сообщением об успешной обработке платежа или с ошибкой в случае проблем.
    """
    data = request.json
    expected_signature = generate_signature(data, SECRET_KEY)

    if data['signature'] != expected_signature:
        return response.json({'message': 'Invalid signature'}, status=400)

    async with get_db() as session:
        user = await payment_service.get_user_by_id(session, data['user_id'])
        if not user:
            return response.json({'message': 'User not found'}, status=404)

        existing_payment = await payment_service.get_payment_by_transaction_id(session, data['transaction_id'])
        if existing_payment:
            return response.json({'message': 'Transaction already processed'}, status=400)

        account = await payment_service.get_account_by_id_and_user_id(session, data['account_id'], data['user_id'])
        if not account:
            account = await payment_service.create_account(session, data['account_id'], data['user_id'])

        try:
            await payment_service.create_payment(session, data['transaction_id'], data['amount'], data['account_id'])
            await payment_service.update_account_balance(session, account, data['amount'])
        except IntegrityError:
            await session.rollback()
            return response.json({'message': 'Failed to process payment'}, status=500)

    return response.json({'message': 'Payment processed successfully'})
