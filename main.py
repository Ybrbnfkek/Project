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