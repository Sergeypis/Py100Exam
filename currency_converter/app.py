# Your API Key: e3f0496a33a63bdd9302078b
import requests
import os
from pprint import pprint
from typing import Optional

key = 'e3f0496a33a63bdd9302078b'
base_currency = 'USD'
hello = 'Добро пожаловать в программу Конвертер валют'
filename_key_access = 'key_access.txt'

print("*" * (len(hello) + 4))
print(f"* {hello} *")
print("*" * (len(hello) + 4))


def read_key_access(filename: str) -> Optional[str]:
    """
    Функция проверяет наличие файла с ключем доступа к сайту обмена валюты.
    :param filename: Имя файла для проверки
    :return: Ключ доступа, строка или None.
    """
    if os.path.exists(filename):
        with open(filename) as f:
            data_key = f.read().strip()
            return None if data_key == '' else data_key

    return None


# url = f"https://v6.exchangerate-api.com/v6/{key}/latest/{base_currency}"
# response = requests.get(url)
# data = response.json()
# pprint(data)


def main():
    read_key_access(filename_key_access)


if __name__ == '__main__':
    main()
