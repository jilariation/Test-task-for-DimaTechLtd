from sanic import response


def all_users_response(users):
    """
    Формирует JSON-ответ для списка пользователей.

    Преобразует список пользователей в формат JSON, включающий их идентификаторы, email, полные имена, статус
    администратора и счета пользователей. Для каждого пользователя создается список его счетов с идентификаторами
    и балансами.

    Аргументы:
    - users: Список объектов User, содержащих информацию о пользователях и их счетах.

    Возвращает:
    - json: JSON-ответ с данными всех пользователей.
    """
    return response.json([{
        'id': user.id,
        'email': user.email,
        'full_name': user.full_name,
        'is_admin': user.is_admin,
        'accounts': [{'id': account.id, 'balance': account.balance} for account in user.accounts]
    } for user in users])


def user_auth_response(user_id, token):
    """
    Формирует JSON-ответ для успешного входа пользователя.

    Создает JSON-ответ, который включает сообщение об успешном входе, идентификатор пользователя и токен.

    Аргументы:
    - user_id: Идентификатор пользователя.
    - token: JWT-токен для авторизованного пользователя.

    Возвращает:
    - json: JSON-ответ с сообщением, идентификатором пользователя и токеном.
    """
    return response.json({
        'message': 'Login successful',
        'user_id': user_id,
        'token': token
    })


def get_user_response(id, email, full_name):
    """
    Формирует JSON-ответ для информации о пользователе.

    Создает JSON-ответ с информацией о пользователе, включая его идентификатор, email и полное имя.

    Аргументы:
    - id: Идентификатор пользователя.
    - email: Email пользователя.
    - full_name: Полное имя пользователя.

    Возвращает:
    - json: JSON-ответ с данными пользователя.
    """
    return response.json({
        'id': id,
        'email': email,
        'full_name': full_name
    })


def get_accounts_response(accounts):
    """
    Формирует JSON-ответ для списка счетов пользователя.

    Преобразует список счетов в формат JSON, включающий идентификаторы счетов и их балансы.

    Аргументы:
    - accounts: Список объектов Account, содержащих информацию о счетах.

    Возвращает:
    - json: JSON-ответ с данными всех счетов.
    """
    return response.json([{
        'id': account.id,
        'balance': account.balance}
        for account in accounts])


def get_payments_response(payments):
    """
    Формирует JSON-ответ для списка платежей пользователя.

    Преобразует список платежей в формат JSON, включающий идентификаторы платежей, суммы и идентификаторы счетов.

    Аргументы:
    - payments: Список объектов Payment, содержащих информацию о платежах.

    Возвращает:
    - json: JSON-ответ с данными всех платежей.
    """
    return response.json([{
        'id': payment.id,
        'amount': payment.amount,
        'account_id': payment.account_id}
        for payment in payments])
