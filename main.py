import os

import json
import requests

source_currency = str(input("Что перевести(код валюты): ").upper().strip())
target_currency = str(input("Во что перевести(код валюты): ").upper().strip())
amount = float(input("Сколько перевести: "))
URL = f"https://api.frankfurter.app/latest?amount={amount}&from={source_currency}&to={target_currency}"

 

try:
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        print(f"{amount} {source_currency} это {data['rates'][target_currency]} {target_currency}")
    else:
        print(f'Не получилось получит данные, ошибка: {response.status_code}')

except requests.exceptions.RequestException as e:
    print(f'Произошла ошибка: {e}')

