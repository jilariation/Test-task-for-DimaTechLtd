from sanic import Request, json

from app.db import get_db
from app.models.user import User
from app.utils.jwt import decode_token
from sqlalchemy.future import select


async def check_admin_permissions(request: Request):
    """
    Проверяет, имеет ли пользователь права администратора.

    Извлекает и декодирует токен из заголовка запроса, затем проверяет, является ли пользователь с указанным
    идентификатором администратором. Если пользователь не найден или не является администратором, возвращает
    ответ с кодом 403 (Forbidden).

    Аргументы:
    - request: Объект запроса Sanic, содержащий заголовок с токеном авторизации.

    Возвращает:
    - json: Ответ с кодом 403, если пользователь не является администратором, иначе None.
    """
    payload = await extract_and_decode_token(request)

    async with get_db() as session:
        result = await session.execute(select(User).where(User.id == payload['user_id']))
        user = result.scalars().first()
        if not user or not user.is_admin:
            return json({'message': 'Forbidden'}, status=403)

    return None


async def extract_and_decode_token(request: Request):
    """
    Извлекает и декодирует токен из заголовка запроса.

    Получает токен из заголовка Authorization, декодирует его и возвращает полезные данные (payload). Если токен
    отсутствует или недействителен, возвращает соответствующий ответ с кодом 401 (Unauthorized).

    Аргументы:
    - request: Объект запроса Sanic, содержащий заголовок с токеном авторизации.

    Возвращает:
    - json или dict: Полезные данные (payload) декодированного токена или ответ с кодом 401 и сообщением об ошибке.
    """
    token = request.headers.get('Authorization')
    if not token:
        return json({'message': 'Unauthorized'}, status=401)

    payload = decode_token(token)
    if 'error' in payload:
        return json({'message': payload['error']}, status=401)

    return payload
