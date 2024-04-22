"""
Данное приложение осуществляет учет и хранение информации о доходах и расходах зарегистрированных пользователей.
"""
import os
import json
from typing import Never, Optional
import string

HELLO_TXT_1 = 'Программа учёта доходов и расходов.'
HELLO_TXT_2 = 'Для работы с программой необходимо войти или зарегистрироваться.'
HELLO_MENU = [
    '1 - Войти со своим логином и паролем.\n',
    '2 - Зарегистрировать нового пользователя.\n',
    '3 - Выйти из программы.'
]
user_filename = 'user.json'


def authorization_menu() -> int:
    print(f"{'*' * (len(HELLO_TXT_2) + 4)}\n"
          f"* {HELLO_TXT_1:^{len(HELLO_TXT_2)}} *\n"
          f"* {HELLO_TXT_2} *\n"
          f"{'*' * (len(HELLO_TXT_2) + 4)}"
          )
    while True:
        print(''.join(HELLO_MENU))

        hello_menu_item = input("Выберите действие: ")
        # os.system('cls' if os.name == 'nt' else 'clear')
        if not hello_menu_item.isdigit() or int(hello_menu_item) > 3 or int(hello_menu_item) < 1:
            print("Необходимо ввести номер пункта 1, 2 или 3. Повторите ввод.")
            continue
        break

    return int(hello_menu_item)


def check_username(username: str) -> Optional[list]:
    try:
        with open(user_filename, 'r', encoding='utf-8') as f:
            dict_users = json.load(f)
            list_user_auth_data = [user for user in dict_users.get('users') if user.get('login') == username]

            return list_user_auth_data

    except (FileNotFoundError, json.JSONDecodeError):
        return None


def add_user(username: str):
    dict_user = dict()
    dict_user['users'] = []
    with open(user_filename, 'w', encoding='utf-8') as file:
        userpass = input("Введите пароль: ")
        dict_user['users'].append({'id': '1', 'login': username, 'password': userpass})
        json.dump(dict_user, file, indent=4)
    return dict_user


def entry_user(text: str):
    username = input(f"{text}\nВведите имя пользователя: ")
    user_auth_data = check_username(username)
    if (user_auth_data is None) or (not user_auth_data):
        count_answer = 0
        while count_answer < 3:
            answer = input("Отсутствуют данные о пользователях. Создать нового пользователя? Y-Да, N-Нет (выход): ").lower()
            if answer == 'y':
                return add_user(username)
            elif answer == 'n':
                exit()
            else:
                print("Неверный ввод!!!")
                count_answer += 1
                continue
        exit()
    elif user_auth_data:
        userpass = input("Введите пароль: ")
        if userpass == user_auth_data[0]['password']:
            print("super")


def authorization_menu_handler():
    match authorization_menu():
        case 1:
            print(entry_user('* Вход в программу *'))
        case 2:
            add_user('* Регистрация пользователя *')
        case 3:
            exit()


def main() -> Never:
    authorization_menu_handler()


if __name__ == '__main__':
    main()
