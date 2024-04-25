"""
Данное приложение осуществляет учет и хранение информации о доходах и расходах зарегистрированных пользователей.
"""
import os
import json
import copy
import string
from typing import Optional

import pickle
from prettytable import PrettyTable


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


def authorization_menu() -> str:
    """
    Функция вывода меню авторизации пользователя. Включаетв себя валидацию введённых значений.
    :return: Строка с номером пункта меню.
    """
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

    return hello_menu_item


def main_menu() -> str:
    """
    Функция вывода главного меню программы. Включаетв себя валидацию введённых значений.
    :return: Строка с номером пункта меню.
    """
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

    return main_menu_item


def read_data_file(filename: str) -> Optional[dict]:
    """
    Функция читает данные пользователей сериализованные в Pickle файл, если он существует.
    :param filename: Имя/путь до файла
    :return: Словарь с данными пользователей
    """
    try:
        with open(filename, 'rb') as pkl_file:
            return pickle.load(pkl_file)
    except OSError:
        print("Ошибка файла данных!!! Обратитесь к разработчику. Программа завершена.")
        exit()


def write_data_file(filename: str, data: dict) -> None:
    """
    Функция сохраняет данные пользователей сериализованные в Pickle файл, если он существует.
    :param filename: Имя/путь до файла
    :param data: Словарь с данными пользователей
    :return: Ничего не возвращает
    """
    try:
        with open(filename, 'wb') as pkl_file:
            pickle.dump(data, pkl_file)
    except OSError:
        print("Ошибка файла данных!!! Обратитесь к разработчику. Программа завершена.")
        exit()


def input_description(text: str) -> str:
    """
    Функция валидации введённой пользователем строки описания/имени пользователя.
    Требуется ввести непустую строку и не пробелы.
    :return: Строка описания.
    """
    text_input_dialog = text
    while True:
        input_value = input(text_input_dialog)
        if input_value.isspace() or input_value == '':
            text_input_dialog = "Недопустимый ввод!!! Повторите попытку: "
            continue
        return input_value


def input_amount_money(text: str) -> str:
    """
    Функция валидации введённых пользователем значений. Требуется ввести только целые числа или float.
    :return: Строка  числа, округленного до 2х знаков после запятой.
    """
    text_input_dialog = text
    input_value = ""
    while True:
        try:
            input_value = input(text_input_dialog)
            input_value = round(float(input_value), 2)
            return str(input_value)
        except (ValueError, TypeError):
            print(f"{input_value}: Неверный ввод!")
            text_input_dialog = "Введите сумму в формате: 123 руб. или 123.45 руб.: "
            continue


def create_new_user_data(username: str) -> None:
    """
    Функция записывает структуру данных нового пользователя в бинарный Pickle файл. Создаёт файл при его отсутствии.
    :param username: Имя текущего пользователя/ login
    :return: Ничего не возвращает
    """
    user_data = dict()
    new_user_data_dict = {  # Структура данных для хранения расходов/доходов текущего пользователя
        'расходы': [
            # {'стол': '12000'},
            # {'стул': '3500'},
            # {'микроволновка': '7800'}
        ],
        'доходы': [
            # {'cash': '14000'},
            # {'продажа': '74000'}
        ]
    }

    income_amount_money = input_amount_money("Введите сумму для учета в 'Доходах': ")
    income_description = input_description("Ведите описание дохода: ")

    if os.path.exists(data_filename):
        user_data = read_data_file(data_filename)

    user_data[username] = new_user_data_dict
    user_data[username]['доходы'].append({income_description: income_amount_money})

    write_data_file(data_filename, user_data)
    print(f"{'*-*-*-' * 10}\n{username}, ваш балланс на текущий момент: {float(income_amount_money):.2f} руб.")


def check_username(username: str) -> Optional[dict]:
    """
    Функция проверяет наличие пользовательских данных (имени пользователя) в файле .json
    :param username: Имя, введённое пользователем при входе или регистрации.
    :return: Словарь с логином и паролем текущего пользователя.
    """
    try:
        with open(user_filename, 'r', encoding='utf-8') as f:
            dict_users = json.load(f)
            list_user_auth_data = [user for user in dict_users.get('users') if user.get('login') == username]

            return None if not list_user_auth_data else list_user_auth_data[0]

    except (FileNotFoundError, json.JSONDecodeError):
        return None


def add_user_json(username: str) -> dict:
    """
    Функция добавляет и сохраняет в файле .json данные для авторизации новых пользователей (логин/пароль).
    :param username: Имя, введённое пользователем при регистрации.
    :return: Словарь с логином и паролем последнего сохранённого пользователя.
    """
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

    return user_data_access['users'][-1]


def entry_user() -> (dict, bool):
    """
    Функция обработчик перврго пункта меню авторизации.Вход в программу по логину и паролю. Производится валидация
    введённых данных, проверка регистрации пользователя, сверка пароля.
    :return: Кортеж: Словарь данных для авторизации текущего пользователя (логин/пароль). Флаг авторизации.
    """
    authorization = False
    count_answer = 0

    while True:
        name_input = input_description("* Вход в программу *\nВведите имя пользователя: ")
        user_auth_data = check_username(name_input)
        if (user_auth_data is None) or (not user_auth_data):
            while True:
                answer = input(f"Отсутствуют данные о пользователе '{name_input}', выберите действие:\n"
                               f"R - ввести заново, N - создать нового , Q - выйти из программы: ").lower()
                match answer:
                    case 'r':
                        break
                    case 'n':
                        return add_user_json(name_input), authorization
                    case 'q':
                        exit()
                    case _:
                        print("Неверный ввод!!!")
                        count_answer += 1
                        if count_answer == 2:
                            exit()
                        continue
        elif user_auth_data:
            authorization = True
            count_pass = 0
            while count_pass < 3:
                userpass = input("Введите пароль: ")
                if userpass == user_auth_data.get('password'):
                    return user_auth_data, authorization
                print("Неверный пароль!!! попробуйте еще раз.")
                count_pass += 1
                continue
            print("Неудачная авторизация. Программа завершена!")
            exit()


def reg_user(text: str) -> dict:
    count_answer = 0
    while True:
        username = input(f"{text}\nВведите имя пользователя: ")
        user_auth_data = check_username(username)
        if (user_auth_data is None) or (not user_auth_data):
            return add_user_json(username)
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


def authorization_menu_handler() -> (dict, bool):
    """
    Функция обработчик меню авторизации пользователя. Производится авторизация или регистрация нового пользователя.
    :return: Кортеж: Словарь данных текущего пользователя. Флаг авторизации.
    """
    current_user = dict()
    authorization = False

    match authorization_menu():
        case '1':  # Вход с логином и паролем
            current_user, authorization = entry_user()
        case '2':  # Регистрация нового пользователя
            current_user = reg_user('* Регистрация пользователя *')
        case '3':  # Выход из программы
            print("Программа завершена.")
            exit()

    return current_user, authorization


def save_pkl_user_data(user_data: dict):
    try:
        with open(data_filename, 'wb') as pkl_file:

            pickle.dump(user_data, pkl_file)
    except OSError:
        print("Ошибка файла данных!!! Обратитесь к разработчику. Программа завершена.")
        exit()


def output_user_data(username: str, user_data: dict):
    table_list = []
    header_table = ['Расходы', 'Сумма, руб. ', 'Доходы', ' Сумма, руб.']
    output_table = PrettyTable()
    output_table.field_names = header_table

    current_user_data = copy.deepcopy(user_data)

    expenses = current_user_data.get('расходы')
    incomes = current_user_data.get('доходы')
    total_expenses = sum([float(*item.values()) for item in expenses])
    total_incomes = sum([float(*item.values()) for item in incomes])
    summ_table_row = ['Итого расходы:', f'{total_expenses:.2f}', 'Итого доходы:', f'{total_incomes:.2f}']

    smaller_list = min(expenses, incomes, key=len)
    bigger_list = max(expenses, incomes, key=len)
    for _ in range(len(bigger_list) - len(smaller_list)):
        smaller_list.append({'': ''})

    for item in range(len(bigger_list)):
        table_list.append(list(*expenses[item].items()) + list(*incomes[item].items()))

    output_table.add_rows(table_list)
    output_table.add_row(['', '', '', ''])
    output_table.add_row(summ_table_row)
    print(f"{'*-*-*-' * 10}\nТаблица учёта Расходов и Доходов пользователя '{username}':")
    print(output_table)


def main_menu_handler(username: str):
    user_data = read_data_file(data_filename)
    current_user_data = user_data[username]
    while True:
        match main_menu():
            case '1':  # Добавить расходы
                expenses_amount_money = input_amount_money(f"{username}, введите сумму для учета в 'Расходах': ")
                expenses_description = input_description("Ведите описание расхода: ")
                current_user_data['расходы'].append({expenses_description: expenses_amount_money})

            case '2':  # Добавить доходы
                income_amount_money = input_amount_money(f"{username}, введите сумму для учета в 'Доходах': ")
                income_description = input_description("Ведите описание дохода: ")
                current_user_data['доходы'].append({income_description: income_amount_money})

            case '3':  # Удалить строку расходов
                del_expenses_name = input_description(f"{username}, введите название 'Расхода' для удаления: ")
                for expense in current_user_data['расходы']:
                    if del_expenses_name in expense:
                        current_user_data['расходы'].remove(expense)

            case '4':  # Удалить строку доходов
                del_income_name = input_description(f"{username}, введите название 'Дохода' для удаления: ")
                for income in current_user_data['доходы']:
                    if del_income_name in income:
                        current_user_data['доходы'].remove(income)

            case '5':  # Выход из программы
                print("Программа завершена.")
                exit()
        output_user_data(username, current_user_data)
        user_data[username] = current_user_data
        save_pkl_user_data(user_data)


def main() -> None:
    current_user, authorization = authorization_menu_handler()  # Авторизация и регистрация пользователя
    username = current_user.get('login')
    if not authorization:
        print(f"{username}, вы успешно зарегистрированы в программе. ")
        create_new_user_data(username)  # Создание файла данных и добавление в него нового пользователя
    else:
        if os.path.exists(data_filename):
            user_data = read_data_file(data_filename)
            if username in user_data:
                output_user_data(username, user_data[username])
            else:
                print(f"{username}, ваши данные были ранее кем-то повреждены, начните учёт заново.")
                create_new_user_data(username)
        else:
            print(f"{username}, ваши данные были ранее кем-то повреждены, начните учёт заново.")
            create_new_user_data(username)

    main_menu_handler(username)


if __name__ == '__main__':
    main()
