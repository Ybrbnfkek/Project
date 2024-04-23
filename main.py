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


# Обработка call - запросы, при нажатии кнопки пользователем.
@bot.callback_query_handler(func=lambda call: button_handler)
def call_back(call):
    # Если получен отклик от кнопки.
    if call.message:
        # Глобальная is_folder_delete- для настройки кнопки на разные функции;
        global is_folder_delete

        # Если получен отклик от кнопки "создать папку".
        if call.data == "Cоздать папку":
            # Глобальная msg, в которой находится стартовое или последнее сообщение бота об итогах действия.
            global msg

            # Глобальная mssg, в которой находится cообщения, которые необходимо удалить при ошибке написания текста.
            global mssg

            # Глобальная choice_handler- для разграничения выбора функции при набирании текста пользователем.
            global choice_handler

            # Глобальная UserDict - для сохранения id пользователя в качестве ключа и название папки и ее содержимого в качестве значения.
            global UserDict

            # Редактированный текст сменяется на сообщение о необходимости ввода данных.
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f"Введите название папки:  ")

            # Меняем значение choice_handler на 2, для правильной обработки текста.
            choice_handler = 2

        # Если получен отклик от кнопки "переместить заметку".
        elif call.data == f"Переместить заметку":
            # Глобальная button_handler - для включения / выключения декоратора, отвечающего на call - запросы.
            global button_handler

            # Меняем button_handler на False, для блокирования нажатия кнопок.
            button_handler = False

            # Глобальная CurrentFolder- для сохранения названия текущей папки в виде строки.
            global CurrentFolder

            # Если в списке папок, 2 или более папки.
            if len(UserDict[user_id].values()) >= 2:
                # Создание additional_keyboard.
                additional_keyboard = create_additional_keyboard(call.from_user.id)

                # Редактированный текст сменяется на сообщение о необходимости ввода данных.
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=additional_keyboard,
                                            text="Введите название заметки, которую хотите переместить и через & папку,откуда переместить и через & папку"
                                                 " куда хотите переметить (пример: хлеб&фильмы&покупки): ")

                # Меняем значение choice_handler на 3, для правильной обработки текста.
                choice_handler = 3

            # Если в списке папок, папок меньше 2.
            else:
                basic_keyboard = create_basic_keyboard(call.from_user.id)

                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=basic_keyboard,
                                            text="Перемещение невозможно/неправильно введенные данные: ")

                # Меняем button_handler на True, для активации нажатия кнопок.
                button_handler = True

        # Если получен отклик от кнопки "удалить папку".
        elif call.data == "Удалить папку":
            # Проверка: не пуст ли список с названиями папок.
            if len(UserDict[user_id]) >= 1:
                # Меняем is_folder_delete на True,  для настройки кнопки навзвания папки на удаление этой папки.
                is_folder_delete = True

                # Создание optional_keyboard.
                optional_keyboard = create_optional_keyboard(call.from_user.id)

                # Редактированный текст сменяется на сообщение о необходимости ввода данных.
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=optional_keyboard,
                                            text="Нажмите на папку, которую хотите удалить:")

            else:
                # Создание additional_keyboard.
                basic_keyboard = create_basic_keyboard(call.from_user.id)

                # Редактированный текст сменяется на сообщение указывающее на ошибку.
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text="Невозможно удалить несуществующие папки",
                                            reply_markup=basic_keyboard)
                # Меняем button_handler на True, для активации нажатия кнопок.
                button_handler = True

        # Если получен отклик от кнопки "удалить заметку".
        elif call.data == "Удалить заметку":
            # Если количество заметок 1 и более.
            if count_notes >= 1:
                # Создание additional_keyboard.
                additional_keyboard = create_additional_keyboard(call.from_user.id)

                # Редактированный текст сменяется на сообщение о необходимости ввода данных.
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=f"Введите название заметки, которую хотите удалить:",
                                            reply_markup=additional_keyboard)

                # Меняем значение choice_handler на 5, для правильной обработки текста.
                choice_handler = 5

            # Если количество заметок меньше 1.
            else:
                # Создание basic_keyboard.
                basic_keyboard = create_basic_keyboard(call.from_user.id)

                # Редактированный текст сменяется на сообщение указывающее на ошибку.
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text="Невозможно удалить несуществующие заметки",
                                            reply_markup=basic_keyboard)

        # Если получен отклик названия папки.
        else:
            # Запоминание нажатия текущей папки.
            CurrentFolder = call.data

            # Если нужно удалить папку.
            if is_folder_delete == True:
                # Удаление папки, выбранной пользователем из словаря.
                del UserDict[user_id][CurrentFolder]

                # Создание basic_keyboard.
                basic_keyboard = create_basic_keyboard(call.from_user.id)

                # Вывод текста, отражающего успех (удаление папки) и basic_keyboard.
                mssg = bot.send_message(call.message.chat.id, "Ваши папки, после удаления:",
                                        reply_markup=basic_keyboard)

                # Удаляем  последнее сообщение, после нажатия кнопки.
                bot.delete_message(chat_id=call.message.chat.id, message_id=msg.message_id)

                # Меняем is_folder_delete на False, для создания новых заметок.
                is_folder_delete = False

            # Если нужно создать заметку.
            else:
                # Меняем значение choice_handler на 6.
                choice_handler = 6

                # Проверка: количество заметок меньше 1.
                if len(UserDict[user_id][CurrentFolder]) < 1:
                    # Редактированный текст сменяется на сообщение о необходимости ввода данных.
                    msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text=f"Выбранная папка {CurrentFolder}" + '\n' "Введите название заметки: ")

                else:
                    msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text=f"Выбранная папка {CurrentFolder}, в ней находится:"
                                                     f" {' '.join(UserDict[user_id][CurrentFolder])}"
                                                     + '\n'"Введите название заметки: ")


