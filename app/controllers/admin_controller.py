from sanic import response, Blueprint
from sanic.request import Request

from app.db import get_db
from app.services import admin_service
from app.utils.token_check import check_admin_permissions
from app.views.responses import all_users_response

bp = Blueprint('admin', url_prefix='/admin')


@bp.post('/users/create')
async def create_user(request: Request):
    """
    Создает нового пользователя.

    Проверяет, обладает ли запрос администраторскими правами. Если нет, возвращает ошибку.
    Если права подтверждены, извлекает данные из запроса и вызывает сервисный метод для создания пользователя.
    Возвращает успешный ответ или сообщение об ошибке.

    Аргументы:
    - request: Sanic Request объект, содержащий данные для создания пользователя.

    Возвращает:
    - JSON-ответ с сообщением об успешном создании пользователя или ошибке.
    """
    error_response = await check_admin_permissions(request)
    if error_response:
        return error_response

    data = request.json
    async with get_db() as session:
        await admin_service.create_user(session, data['email'], data['full_name'], data['password'])
        return response.json({'message': 'User created successfully'})


@bp.delete('/users/delete/<user_id>')
async def delete_user(request: Request, user_id: int):
    """
    Удаляет пользователя по указанному идентификатору.

    Проверяет, обладает ли запрос администраторскими правами. Если нет, возвращает ошибку.
    Если права подтверждены, вызывает сервисный метод для удаления пользователя.
    Возвращает успешный ответ или сообщение об ошибке, если пользователь не найден.

    Аргументы:
    - request: Sanic Request объект.
    - user_id: Идентификатор пользователя, которого нужно удалить.

    Возвращает:
    - JSON-ответ с сообщением об успешном удалении пользователя или ошибке, если пользователь не найден.
    """
    error_response = await check_admin_permissions(request)
    if error_response:
        return error_response

    async with get_db() as session:
        success = await admin_service.delete_user(session, user_id)
        if success:
            return response.json({'message': 'User deleted successfully'})
        return response.json({'message': 'User not found'}, status=404)


@bp.put('/users/update/<user_id>')
async def update_user(request: Request, user_id: int):
    """
    Обновляет информацию о пользователе по указанному идентификатору.

    Проверяет, обладает ли запрос администраторскими правами. Если нет, возвращает ошибку.
    Если права подтверждены, извлекает данные из запроса и вызывает сервисный метод для обновления пользователя.
    Возвращает успешный ответ или сообщение об ошибке, если пользователь не найден.

    Аргументы:
    - request: Sanic Request объект, содержащий обновленные данные пользователя.
    - user_id: Идентификатор пользователя, информацию о котором нужно обновить.

    Возвращает:
    - JSON-ответ с сообщением об успешном обновлении пользователя или ошибке, если пользователь не найден.
    """
    error_response = await check_admin_permissions(request)
    if error_response:
        return error_response

    data = request.json
    async with get_db() as session:
        success = await admin_service.update_user(session, user_id, data.get('email'), data.get('full_name'),
                                                  data.get('password'))
        if success:
            return response.json({'message': 'User updated successfully'})
        return response.json({'message': 'User not found'}, status=404)


@bp.get('/users')
async def get_users(request: Request):
    """
    Возвращает список всех пользователей.

    Проверяет, обладает ли запрос администраторскими правами. Если нет, возвращает ошибку.
    Если права подтверждены, вызывает сервисный метод для получения списка пользователей.
    Возвращает JSON-ответ с данными всех пользователей.

    Аргументы:
    - request: Sanic Request объект.

    Возвращает:
    - JSON-ответ со списком пользователей.
    """
    error_response = await check_admin_permissions(request)
    if error_response:
        return error_response

    async with get_db() as session:
        users = await admin_service.get_users(session)
        return all_users_response(users)
