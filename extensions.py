import requests
import json
from config import keys

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}')
        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты: {base}.')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}')

        req_text = f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}'
        req = requests.get(req_text)
        result = json.loads(req.content)[keys[base]] * int(amount)
        return result