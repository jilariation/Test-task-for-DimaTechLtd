from sanic import response, Blueprint
from sanic.request import Request

from app.db import get_db
from app.services import user_service
from app.utils.token_check import extract_and_decode_token
from app.views.responses import get_user_response, get_accounts_response, get_payments_response

bp = Blueprint('user', url_prefix='/user')


@bp.get('/about')
async def get_user(request: Request):
    """
    Получение информации о пользователе.

    Извлекает и декодирует токен из заголовков запроса, чтобы получить идентификатор пользователя (`user_id`). Затем выполняет следующие действия:
    1. Запрашивает данные пользователя по идентификатору `user_id`.
    2. Если пользователь найден, возвращает его информацию в формате JSON.
    3. Если пользователь не найден, возвращает ошибку 404.

    Аргументы:
    - request: Sanic Request объект, содержащий токен в заголовках.

    Возвращает:
    - JSON-ответ с данными пользователя или с ошибкой в случае его отсутствия.
    """
    payload = await extract_and_decode_token(request)
    user_id = payload['user_id']

    async with get_db() as session:
        user = await user_service.get_user_by_id(session, user_id)
        if user:
            return get_user_response(user.id, user.email, user.full_name)
        return response.json({'message': 'User not found'}, status=404)


@bp.get('/accounts')
async def get_user_accounts(request: Request):
    """
    Получение счетов пользователя.

    Извлекает и декодирует токен из заголовков запроса, чтобы получить идентификатор пользователя (`user_id`). Затем выполняет следующие действия:
    1. Запрашивает все счета пользователя по идентификатору `user_id`.
    2. Возвращает информацию о счетах в формате JSON.

    Аргументы:
    - request: Sanic Request объект, содержащий токен в заголовках.

    Возвращает:
    - JSON-ответ с данными счетов пользователя.
    """
    payload = await extract_and_decode_token(request)
    user_id = payload['user_id']

    async with get_db() as session:
        accounts = await user_service.get_accounts_by_user_id(session, user_id)
        return get_accounts_response(accounts)


@bp.get('/payments')
async def get_user_payments(request: Request):
    """
    Получение платежей пользователя.

    Извлекает и декодирует токен из заголовков запроса, чтобы получить идентификатор пользователя (`user_id`). Затем выполняет следующие действия:
    1. Запрашивает все платежи пользователя по идентификатору `user_id`.
    2. Возвращает информацию о платежах в формате JSON.

    Аргументы:
    - request: Sanic Request объект, содержащий токен в заголовках.

    Возвращает:
    - JSON-ответ с данными платежей пользователя.
    """
    payload = await extract_and_decode_token(request)
    user_id = payload['user_id']

    async with get_db() as session:
        payments = await user_service.get_payments_by_user_id(session, user_id)
        return get_payments_response(payments)
