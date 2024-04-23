"""
Данное приложение осуществляет учет и хранение информации о доходах и расходах зарегистрированных пользователей.
"""
import os
from pprint import pprint
import pickle
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
data_filename = 'data.pkl'
new_user_data_dict = {
    'расходы': [
    ],
    'доходы': [
    ]
}


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


def create_new_user_data(user_data_access: dict):
    user_data = dict()
    username = user_data_access.get('login')
    income_amount_money = input(
        f"{username}, вы успешно зарегистрированы в программе. Введите сумму для учета в 'Доходах': ")
    income_description = input("Ведите описание дохода: ")

    if os.path.exists(data_filename):
        with open(data_filename, 'rb') as pkl_file:
            user_data = pickle.load(pkl_file)

    user_data[username] = new_user_data_dict
    user_data[username]['доходы'].append({income_description: income_amount_money})

    with open(data_filename, 'wb') as pkl_file:
        pickle.dump(user_data, pkl_file)


def check_username(username: str) -> Optional[dict]:
    try:
        with open(user_filename, 'r', encoding='utf-8') as f:
            dict_users = json.load(f)
            list_user_auth_data = [user for user in dict_users.get('users') if user.get('login') == username]

            return list_user_auth_data[0]

    except (FileNotFoundError, json.JSONDecodeError):
        return None


def add_user(username: str) -> list:
    user_data_access = dict()
    user_data_access['users'] = []
    userpass = input("Введите пароль: ")
    try:
        with open(user_filename, 'r', encoding='utf-8') as file_read:
            user_data_access = json.load(file_read)
            user_data_access['users'].append({'login': username, 'password': userpass})
        with open(user_filename, 'w', encoding='utf-8') as file_write:
            json.dump(user_data_access, file_write, indent=4)

    except (FileNotFoundError, json.JSONDecodeError):
        with open(user_filename, 'w', encoding='utf-8') as file:
            user_data_access['users'].append({'login': username, 'password': userpass})
            json.dump(user_data_access, file, indent=4)

    # create_new_user_data(user_data_access['users'][-1])
    return user_data_access['users'][-1]


def entry_user(text: str):
    authorization = False
    count_answer = 0
    username = input(f"{text}\nВведите имя пользователя: ")
    user_auth_data = check_username(username)
    if (user_auth_data is None) or (not user_auth_data):
        while count_answer < 3:
            answer = input(
                f"Отсутствуют данные о пользователе '{username}'. Создать нового? Y-Да, N-Нет (Выход): ").lower()
            match answer:
                case 'y':
                    return add_user(username), authorization
                case 'n':
                    exit()
                case _:
                    print("Неверный ввод!!!")
                    count_answer += 1
                    continue
        exit()
    elif user_auth_data:
        authorization = True
        userpass = input("Введите пароль: ")
        if userpass == user_auth_data.get('password'):
            print("super")
            return user_auth_data, authorization


def reg_user(text: str) -> list:
    count_answer = 0
    while True:
        username = input(f"{text}\nВведите имя пользователя: ")
        user_auth_data = check_username(username)
        if (user_auth_data is None) or (not user_auth_data):
            return add_user(username)
        elif user_auth_data:
            while True:
                answer = input(
                    f"Пользователь с именем '{username}' уже существует. Ввести заново? Y-Да, N-Нет (Выход): ").lower()
                match answer:
                    case 'y':
                        break
                    case 'n':
                        exit()
                    case _:
                        print("Неверный ввод!!!")
                        count_answer += 1
                        if count_answer == 3:
                            exit()
                        continue


def authorization_menu_handler():
    match authorization_menu():
        case 1:
            current_user, authorization = entry_user('* Вход в программу *')
            return current_user, authorization
        case 2:
            current_user = reg_user('* Регистрация пользователя *')
            authorization = False
            return current_user, authorization
        case 3:
            exit()


def output_user_data():
    pass


def main_menu_handler():
    pass


def main() -> Never:
    current_user, authorization = authorization_menu_handler()  # Авторизация и регистрация пользователя
    if not authorization:
        create_new_user_data(current_user)  # Создание файла данных и добавление в него нового пользователя
    output_user_data()
    main_menu_handler()


if __name__ == '__main__':
    main()
