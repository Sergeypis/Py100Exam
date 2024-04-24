"""
Данное приложение осуществляет учет и хранение информации о доходах и расходах зарегистрированных пользователей.
"""
import os
from pprint import pprint
from prettytable import PrettyTable
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
MAIN_MENU_HD = 'Главное меню'
MAIN_MENU = [
    '1 - Добавить расходы.\n',
    '2 - Добавить средства на балланс.\n',
    '3 - Удалить строку расходов.\n',
    '4 - Удалить строку доходов.\n',
    '5 - Выйти из программы'
]
user_filename = 'user.json'
data_filename = 'data.pkl'
new_user_data_dict = {
    'расходы': [
        {'стол': '12000'},
        {'стул': '3500'},
        {'микроволновка': '7800'}
    ],
    'доходы': [
        #{'cash': '14000'},
        #{'продажа наркоты': '74000'}
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


def main_menu() -> int:
    print(f"{'*' * (len(MAIN_MENU_HD) + 20)}\n"
          f"* {MAIN_MENU_HD:^{len(MAIN_MENU_HD) + 16}} *\n"
          f"{'*' * (len(MAIN_MENU_HD) + 20)}"
          )
    while True:
        print(''.join(MAIN_MENU))

        main_menu_item = input("Выберите действие: ")
        # os.system('cls' if os.name == 'nt' else 'clear')
        if not main_menu_item.isdigit() or int(main_menu_item) > 5 or int(main_menu_item) < 1:
            print("Необходимо ввести номер пункта от 1 до 5. Повторите ввод.")
            continue
        break

    return int(main_menu_item)


def create_new_user_data(user_data_access: dict):
    user_data = dict()
    username = user_data_access.get('login')
    income_amount_money = input(f"{username}, вы успешно зарегистрированы в программе. "
                                f"Введите сумму для учета в 'Доходах': ")
    income_description = input("Ведите описание дохода: ")

    if os.path.exists(data_filename):
        with open(data_filename, 'rb') as pkl_file:
            user_data = pickle.load(pkl_file)

    user_data[username] = new_user_data_dict
    user_data[username]['доходы'].append({income_description: income_amount_money})

    with open(data_filename, 'wb') as pkl_file:
        pickle.dump(user_data, pkl_file)

    return float(income_amount_money)


def check_username(username: str) -> Optional[dict]:
    try:
        with open(user_filename, 'r', encoding='utf-8') as f:
            dict_users = json.load(f)
            list_user_auth_data = [user for user in dict_users.get('users') if user.get('login') == username]

            return None if not list_user_auth_data else list_user_auth_data[0]
            # return list_user_auth_data[0]

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
        count_pass = 0
        while count_pass < 3:
            userpass = input("Введите пароль: ")
            if userpass == user_auth_data.get('password'):
                print("super")
                return user_auth_data, authorization
            print("Неверный пароль!!! попробуйте еще раз.")
            count_pass += 1
            continue
        print("Неудачная авторизация. Программа завершена!")
        exit()


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


def read_user_data(username: str):
    try:
        with open(data_filename, 'rb') as pkl_file:
            user_data = pickle.load(pkl_file)

        return user_data[username]
    except OSError:
        return None


def output_user_data(username: str):
    table_list = []
    header_table = ['Расходы', 'Сумма, руб. ', 'Доходы', ' Сумма, руб.']
    output_table = PrettyTable()
    output_table.field_names = header_table

    current_user_data = read_user_data(username)
    if current_user_data is None:
        print("Ошибка файла данных!!! Обратитесь к разработчику. Программа завершена.")
        exit()
    expenses = current_user_data.get('расходы')
    incomes = current_user_data.get('доходы')
    total_expenses = sum([int(*item.values()) for item in expenses])
    total_incomes = sum([int(*item.values()) for item in incomes])
    summ_table_row = ['Итого расходы:', total_expenses, 'Итого доходы:', total_incomes]

    smaller_list = min(expenses, incomes, key=len)
    bigger_list = max(expenses, incomes, key=len)
    for _ in range(len(bigger_list) - len(smaller_list)):
        smaller_list.append({'': ''})

    for item in range(len(bigger_list)):
        table_list.append(list(*expenses[item].items()) + list(*incomes[item].items()))

    output_table.add_rows(table_list)
    output_table.add_row(['', '', '', ''])
    output_table.add_row(summ_table_row)
    print(output_table)


def main_menu_handler():
    print(main_menu())


def main() -> Never:
    current_user, authorization = authorization_menu_handler()  # Авторизация и регистрация пользователя
    if not authorization:
        cash_new_user = create_new_user_data(current_user)  # Создание файла данных и добавление в него нового пользователя
        print(f"{current_user.get('login')}, ваш балланс на текущий момент: {cash_new_user:.2f} руб.")
    else:
        print(f"Таблица учёта Расходов и Доходов пользователя '{current_user.get('login')}':")
        output_user_data(current_user.get('login'))

    main_menu_handler()


if __name__ == '__main__':
    main()
