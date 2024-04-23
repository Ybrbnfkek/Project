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

# Создаем additional_keyboard, в отличие от основной показывает не только названия папок, но и их содержимое.
def create_additional_keyboard(UserID: int):
    additional_keyboard = types.InlineKeyboardMarkup()
    for name_folder in UserDict[UserID].keys():
        name_folder = types.InlineKeyboardButton(text=f"📁{name_folder}: {' '.join(UserDict[UserID][name_folder])}",
                                                 callback_data=f'{name_folder}')

        additional_keyboard.add(name_folder)

    # Создание и добавление кнопок 'создать папку', 'переместить заметку' на клавиатуру.
    additional_keyboard.add(types.InlineKeyboardButton(text='➕Cоздать папку', callback_data='Cоздать папку'),
                            types.InlineKeyboardButton(text='➡️Переместить заметку',
                                                       callback_data='Переместить заметку'))

    # Создание и добавление кнопок 'удалить папку', 'удалить заметку' на клавиатуру.
    additional_keyboard.add(types.InlineKeyboardButton(text='❌Удалить папку', callback_data='Удалить папку'),
                            types.InlineKeyboardButton(text='🗑Удалить заметку', callback_data='Удалить заметку'))

    return additional_keyboard



# Создаем optional_keyboard, которая показывает только названия папок.
def create_optional_keyboard(UserID: int):
    optional_keyboard = types.InlineKeyboardMarkup()

    for name_folder in UserDict[UserID].keys():
        name_folder = types.InlineKeyboardButton(text=f"📁{name_folder}", callback_data=f'{name_folder}')

        optional_keyboard.add(name_folder)

    return optional_keyboard

# Функция для команду /start- выводит basic_keyboard и ознакомительный текст, о принципах работы бота.
@bot.message_handler(commands=['start'])
def start_bot(message):
    # Глобальная mssg, в которой находится cообщения, которые необходимо удалить при ошибке написания текста.
    global mssg

    # Глобальная UserDict - для сохранения id пользователя в качестве ключа и название папки и ее содержимого в качестве значения.
    global UserDict

    # Глобальная user_id - для хранения id пользователя.
    global user_id

    # Сохранение текущего id пользователя.
    user_id = message.from_user.id

    # Cоздание UserDict определенного id пользователя.
    UserDict[user_id] = dict()

    # Вывод клавиатуры после нажатия ввода /start.
    basic_keyboard = create_basic_keyboard(message.from_user.id)

    # Вывод ознакомительного текста и basic_keyboard.
    mssg = bot.send_message(message.chat.id, f'{message.from_user.username}, я бот-организатор заметок.'
                                             f' Чтобы создать заметку нажмите на кнопку "создать папку" и введите название папки,'
                                             f' а затем нажмите на кнопку созданной папки и введите необходимую заметку.',
                            reply_markup=basic_keyboard)


# Функция, работающая при нажатии команды contacts- и вывод текста с ссылкой для связи.
@bot.message_handler(commands=['contacts'])
def help_bot(message):
    # Глобальная mssg, в которой находится cообщения, которые необходимо удалить при ошибке написания текста.
    global mssg

    # Вывод клавиатуры после нажатия ввода /contacts.
    basic_keyboard = create_basic_keyboard(message.from_user.id)

    # Вывод текста и  basic_keyboard с ссылкой для связи.
    mssg = bot.send_message(message.chat.id, "По всем вопросам обращаться https://t.me/sleep_fox789",
                            reply_markup=basic_keyboard)


