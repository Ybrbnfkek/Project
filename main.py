from dublib.Methods import CheckPythonMinimalVersion, ReadJSON
from telebot import types

import json
import os
import telebot


CheckPythonMinimalVersion(3, 11)

# Проверяет существование папки UserData.
if os.path.exists("UserData") is False:
    # Создание папки, если таковой нет.
    os.mkdir("UserData")

Settings = ReadJSON("Settings.json")

# Передаем боту токен.
bot = telebot.TeleBot(Settings["token"])

# Глобальную UserDict - для сохранения id пользователя в качестве ключа и название папки и ее содержимого в качестве значения;
UserDict = dict()

# Глобальную CurrentFolder - для сохранения названия текущей папки в виде строки;
CurrentFolder = ''

# Глобальную count_notes- для вычисления количества заметок;
count_notes = 0

# Глобальную button_handler- для включения/выключения декоратора, отвечающего на call-запросы;
button_handler = True

# Глобальную is_folder_delete- для настройки кнопки на разные функции;
is_folder_delete = False

# Создаем basic_keyboard для хранения id пользователя, и названия текущей папки.
def create_basic_keyboard(UserID: int):
    # Создание InlineKeyboard.
    basic_keyboard = types.InlineKeyboardMarkup()

    # Итерация всех названий папок.
    for name_folder in UserDict[UserID].keys():
        # Создание на каждую папку из списка кнопки.
        name_folder = types.InlineKeyboardButton(text=f"📁{name_folder}", callback_data=f'{name_folder}')

        basic_keyboard.add(name_folder)

    # Создание и добавление кнопок 'создать папку', 'переместить заметку' на клавиатуру.
    basic_keyboard.add(types.InlineKeyboardButton(text='➕Cоздать папку', callback_data='Cоздать папку'),
                       types.InlineKeyboardButton(text='➡️Переместить заметку', callback_data='Переместить заметку'))

    # Создание и добавление кнопок 'удалить папку', 'удалить заметку' на клавиатуру.
    basic_keyboard.add(types.InlineKeyboardButton(text='❌Удалить папку', callback_data='Удалить папку'),
                       types.InlineKeyboardButton(text='🗑Удалить заметку', callback_data='Удалить заметку'))

    # Вывод клавиатуры.
    return basic_keyboard