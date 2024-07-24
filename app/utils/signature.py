import hashlib


def generate_signature(data: dict, secret_key: str) -> str:
    """
    Генерация подписи для проверки целостности данных.

    Создает подпись для данных, используя SHA-256 хеширование и секретный ключ.
    Подпись формируется из строки, которая состоит из значений полей данных в определенном порядке и секретного ключа.

    Аргументы:
    - data: Словарь с данными, для которых требуется создать подпись. Ожидается, что словарь содержит ключи 'account_id',
      'amount', 'transaction_id', и 'user_id'.
    - secret_key: Секретный ключ, используемый для создания подписи.

    Возвращает:
    - str: Хешированная подпись в шестнадцатеричном формате.
    """
    sign_str = f"{data['account_id']}{data['amount']}{data['transaction_id']}{data['user_id']}{secret_key}"
    return hashlib.sha256(sign_str.encode()).hexdigest()
