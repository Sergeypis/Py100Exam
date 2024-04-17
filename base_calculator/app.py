""" Программа - генератор случайных паролей"""

import string
from random import sample, shuffle


def initial_data() -> tuple[int, str]:
    """
    Функция производит валидацию введенных пользователем значений длины пароля и спецсимволов
    :return: Целое число - длина пароля
             Список спецсимволов для генерации пароля
    """

    print("Добро пожаловать в программу по генерации случайных паролей!")

    while True:
        print("." * 100)
        password_len = input("Введите длину желаемого пароля более 5 символов: ")
        if not password_len.isdigit():
            print("Нужно ввести только целое число!!!")
            continue

        if int(password_len) < 6:
            print("Пароль должен быть более 5 символов!!!")
            continue
        password_len = int(password_len)
        break

    set_all_spec_symbols = string.punctuation
    set_all_spec_symbols = set(set_all_spec_symbols)
    set_all_spec_symbols.add('№')
    while True:
        print("-" * 100)
        spec_symbols = input("Введите спецсимволы, если их нужно использовать в пароле. Иначе нажмите Ввод: ")
        spec_symbols = set(spec_symbols)

        if ' ' in spec_symbols or not spec_symbols.issubset(set_all_spec_symbols):
            print("Нужно ввести только спецсимволы, без пробелов!!!")
            continue

        if len(spec_symbols) > password_len:
            print("Количество спецсимволов не может быть больше длины пароля. Повторите ввод!!!")
            continue
        break

    spec_symbols = ''.join(spec_symbols)
    print("-" * 100)
    if spec_symbols:
        print(f"Будет сгенерирован пароль из '{password_len - len(spec_symbols)}' символов и спецсимволов {spec_symbols}")
    else:
        print(f"Будет сгенерирован пароль из '{password_len}' символов")

    return password_len, spec_symbols


def generator(password_len: int = 5, spec_symbols: str = '') -> list:
    """
    Функция генерирует последовательность случайных символов из букв, цифр и спецсимволов.
    :param password_len: Длина пароля
    :param spec_symbols: Используемые спецсимволы
    :return: Последовательность случайных символов
    """

    list_symbols = sample(
        string.digits +
        string.ascii_lowercase +
        string.ascii_uppercase,
        password_len - len(spec_symbols))

    list_symbols = list_symbols + list(spec_symbols)
    shuffle(list_symbols)

    return list_symbols


def main() -> None:
    """
    Главная функция генератора случайной последовательности.
    :return: None
    """
    password_len, spec_symbols = initial_data()
    password = generator(password_len, spec_symbols)

    filename = input("Введите имя файла для сохранения пароля или нажмите Ввод если пароль нужно только показать: ")
    if not filename:
        print("*" * 100)
        print(f"Ваш сгенерированый пароль: {''.join(password)}")
    else:
        with open(filename, 'w', encoding='utf-8') as secret_file:
            secret_file.writelines(''.join(password))
        print("*" * 100)
        print(f"Создан файл {filename} с паролем.")


if __name__ == '__main__':
    main()

