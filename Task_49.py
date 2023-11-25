# Создать телефонный справочник с
# возможностью импорта и экспорта данных в
# формате .txt. Фамилия, имя, отчество, номер
# телефона - данные, которые должны находиться
# в файле.
# 1. Программа должна выводить данные
# 2. Программа должна сохранять данные в
# текстовом файле
# 3. Пользователь может ввести одну из
# характеристик для поиска определенной
# записи(Например имя или фамилию
# человека)
# 4. Использование функций. Ваша программа
# не должна быть линейной

from csv import DictReader, DictWriter, reader, writer
from os.path import exists
from os import path

file_name = 'phones.csv'

class lenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt

def get_info():

    nameValid = False
    while not nameValid:
        firstName = input('Введите имя: ')
        if len(firstName) == 0:
            print('Вы не ввели имя')
        else:
            nameValid = True

    lastName = 'Иванов'
    phoneNumber = None

    is_valid = False

    while not is_valid:
        try:
            phoneNumber = int(input('Введите номер: '))
            if len(str(phoneNumber)) != 11:
               raise lenNumberError("Неверная длина номера")
            else:
                is_valid = True
        except ValueError:
            print('Не валидный номер')
        except lenNumberError as err:
            print(err)
            continue


    return [firstName, lastName, phoneNumber]


def createFile(file_name):
    with open(file_name, 'w', encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия','Телефон'])
        f_writer.writeheader()


def write_file(lst):
    with open(file_name, 'r', encoding='utf-8') as data:
        f_reader = DictReader(data)
        res = list(f_reader)

    values = [el['Телефон'] for el in res]

    if str(lst[2]) in values:
        print("Такой номер уже существует")
        return

    obj = {'Имя': lst[0], 'Фамилия': lst[1], 'Телефон': lst[2]}

    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        res.append(obj)
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия','Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)


def readFile(file_name):
    with open(file_name, 'r', encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)

def copyData(source_filename, destination_filename, row_number):

    # Проверяем, существует ли файл-источник
    if not path.exists(source_filename):
        print("Файл-источник не существует.")
        return

    # Открываем файл-источник для чтения
    with open(source_filename, 'r', encoding='utf-8', newline='') as source_file:
        csv_reader = reader(source_file)
        data = list(csv_reader)

        # Проверяем, есть ли строка с указанным номером
        if row_number <= 0 or row_number > len(data):
            print("Указан неверный номер строки.")
            return

        # Выводим содержимое строки для проверки
        print(f"Содержимое строки {row_number}:")
        print(data[row_number - 1])

        # Пользовательский выбор для копирования данных
        choice = input("Хотите скопировать данные (Y/N)? ").strip().upper()

        if choice == 'Y':
            # Открываем файл-назначение для записи
            mode = 'a' if path.exists(destination_filename) else 'w'
            with open(destination_filename, mode, newline='', encoding='utf-8') as dest_file:
                csv_writer = writer(dest_file)
                # Копируем строку в файл-назначение
                csv_writer.writerow(data[row_number - 1])
                print("Данные успешно скопированы.")
        else:
            print("Данные не были скопированы.")

def main():
    while True:
        command = input('Введите команду: ').lower()

        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                createFile(file_name)
            write_file(get_info())
        elif command == 'r':
            if not exists(file_name):
                print("Файл не создан!")
                continue
            print(*readFile(file_name))
        # Функция копирования строки в новый файл (Домашняя работа)
        elif command == 'c':
            # Получаем от пользователя названия файлов и номер строки
            destinationFileName = input("Введите название файла-назначения: ")
            rowToCopy = int(input("Введите номер строки для копирования: "))

            # Вызываем функцию для копирования данных
            copyData('phones.csv', destinationFileName, rowToCopy)


main()
