from sanic import response, Request, Blueprint
from app.services import auth_service
from app.db import get_db
from app.utils.jwt import create_token
from app.views.responses import user_auth_response

bp = Blueprint('auth')


@bp.post('/register')
async def register(request: Request):
    """
    Регистрация нового пользователя.

    Принимает данные пользователя (email, full_name, password) из тела запроса и пытается зарегистрировать пользователя,
    вызывая метод `register_user` сервиса аутентификации. Если регистрация успешна, возвращает сообщение об успешной
    регистрации. В случае ошибки возвращает сообщение об ошибке и статус 400.

    Аргументы:
    - request: Sanic Request объект, содержащий данные для регистрации пользователя.

    Возвращает:
    - JSON-ответ с сообщением об успешной регистрации или ошибке.
    """
    data = request.json
    async with get_db() as session:
        user, error = await auth_service.register_user(session, data['email'], data['full_name'], data['password'])
        if error:
            return response.json({'message': error}, status=400)
        return response.json({'message': 'User registered successfully'}, status=201)


@bp.post('/login')
async def login(request: Request):
    """
    Аутентификация пользователя и получение JWT-токена.

    Принимает данные для аутентификации (email, password) из тела запроса и пытается войти в систему,
    вызывая метод `login_user` сервиса аутентификации. Если пользователь успешно аутентифицирован, создается
    JWT-токен, и возвращается ответ с информацией о пользователе и токене. В случае ошибки возвращает
    сообщение о неверных учетных данных и статус 400.

    Аргументы:
    - request: Sanic Request объект, содержащий данные для аутентификации пользователя.

    Возвращает:
    - JSON-ответ с информацией о пользователе и JWT-токене, если аутентификация успешна.
    - JSON-ответ с сообщением об ошибке и статусом 400, если аутентификация не удалась.
    """
    data = request.json
    async with get_db() as session:
        user, authenticated = await auth_service.login_user(session, data['email'], data['password'])
        if authenticated:
            is_admin = getattr(user, 'is_admin', False)
            token = create_token(user.id, is_admin)
            return user_auth_response(user.id, token)
        return response.json({'message': 'Invalid credentials'}, status=400)
