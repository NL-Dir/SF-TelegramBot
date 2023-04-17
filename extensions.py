import requests
import json

from config import API_KEY, keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты: {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}')

        r = requests.get(f'https://api.currencyapi.com/v3/latest?apikey={API_KEY}'
                         f'&currencies={base_ticker}&base_currency={quote_ticker}')
        total = float(json.loads(r.content)["data"][base_ticker]["value"]) * amount
        return total
