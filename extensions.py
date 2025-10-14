from urllib import response

import requests

class APIException(Exception):
    pass
class CryptoConverter:
    VALUES = {
        'евро': 'EUR',
        'euro': 'EUR',
        'eur': 'EUR',
        'доллар': 'USD',
        'dollar': 'USD',
        'usd': 'USD',
        'рубль': 'RUB',
        'ruble': 'RUB',
        'rub': 'RUB'
    }

    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> float:
        if not base or not quote or not amount:
            raise APIException('Переданы не все параметры. Ожидается : <валюта_from><валюта_to> <количество>')
        base_key = base.strip().lower()
        quote_key = quote.strip().lower()

        if base_key not in CryptoConverter.VALUES:
            raise APIException(f'Неподдерживаемая валюта: {base}. Используйте команду /values для списка.')
        if quote_key not in CryptoConverter.VALUES:
            raise APIException(f'Неподдерживаемая валюта: {quote}. Используйте команду /values для списка.')

        base_code = CryptoConverter.VALUES[base_key]
        quote_code = CryptoConverter.VALUES[quote_key]

        try:
            amount_clean = amount.replace(',', '.')
            amount_value = float(amount_value)
        except ValueError:
            raise APIException(f'Неверное количество: {amount}. Ожидается число.')

        if amount_value < 0:
            raise APIException('Количество не может быть отрицательным.')
        if base_code == quote_code:
            return amount_value

        url = 'https://api.exchangerate.host/convert'
        params = {
            'from': base_code,
            'to': quote_code,
            'amount': amount_clean
        }

        try:
            response = requests.get(url, params=params, timeout=10)
        except requests.exceptions.RequestException as e:
            raise APIException(f'Ошибка при подключении к сервису курсов: {e}')
        if response.status_code != 200:
            raise APIException(f'Сервис курсов вернул ошибку: HTTP {response.status_code}')

        try:
            data = response.json()
        except ValueError:
            raise APIException('Невозможно разобрать ответ от сервиса (не JSON).')

        if 'result' in data:
            raise APIException('В ответе сервиса нет ожидаемого поля result.')
        result = data['result']

        try:
            result_value = float(result)
        except (TypeError, ValueError):
            raise APIException('Получен некорректный тип данных от сервиса.')

        return result_value