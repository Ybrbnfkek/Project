from dublib.Methods import CheckPythonMinimalVersion, ReadJSON
from telebot import types

import json
import os
import telebot

# Проверка поддержки используемой версии Python.
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
    basic_keyboard = types.InlineKeyboardMarkup()

    for name_folder in UserDict[UserID].keys():
        name_folder = types.InlineKeyboardButton(text=f"📁{name_folder}", callback_data=f'{name_folder}')

        basic_keyboard.add(name_folder)

    basic_keyboard.add(types.InlineKeyboardButton(text='➕Cоздать папку', callback_data='Cоздать папку'),
                       types.InlineKeyboardButton(text='➡️Переместить заметку', callback_data='Переместить заметку'))

    basic_keyboard.add(types.InlineKeyboardButton(text='❌Удалить папку', callback_data='Удалить папку'),
                       types.InlineKeyboardButton(text='🗑Удалить заметку', callback_data='Удалить заметку'))

    return basic_keyboard

# Создаем additional_keyboard, в отличие от основной показывает не только названия папок, но и их содержимое.
def create_additional_keyboard(UserID: int):
    additional_keyboard = types.InlineKeyboardMarkup()

    for name_folder in UserDict[UserID].keys():
        name_folder = types.InlineKeyboardButton(text=f"📁{name_folder}: {' '.join(UserDict[UserID][name_folder])}",
                                                 callback_data=f'{name_folder}')

        additional_keyboard.add(name_folder)

    additional_keyboard.add(types.InlineKeyboardButton(text='➕Cоздать папку', callback_data='Cоздать папку'),
                            types.InlineKeyboardButton(text='➡️Переместить заметку',
                                                       callback_data='Переместить заметку'))

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

# Функция команды /start- выводит basic_keyboard и ознакомительный текст, о принципах работы бота.
@bot.message_handler(commands=['start'])
def start_bot(message):
    global mssg

    global UserDict

    global user_id

    user_id = message.from_user.id

    UserDict[user_id] = dict()

    basic_keyboard = create_basic_keyboard(message.from_user.id)

    mssg = bot.send_message(message.chat.id, f'{message.from_user.username}, я бот-организатор заметок.'
                                             f' Чтобы создать заметку нажмите на кнопку "создать папку", введите название папки,'
                                             f' а затем нажмите на кнопку созданной папки и введите необходимую заметку. Если нужно удалить папку или заметку нажмите на соотвествующие кнопки.\nЧтобы узнать команды бота используйте /help',
                            reply_markup=basic_keyboard)

# Функция, работающая при нажатии команды contacts- и вывод текста с ссылкой для связи.
@bot.message_handler(commands=['contacts'])
def help_bot(message):
    global mssg

    basic_keyboard = create_basic_keyboard(message.from_user.id)

    mssg = bot.send_message(message.chat.id, "По всем вопросам обращаться https://t.me/LoLCaKe",
                            reply_markup=basic_keyboard)

# handles the /help command
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,
                 f'/start - начать взаимодействие с ботом.\n/contacts - для связи с автором.\nостальное тыкать на кнопочки')


# starts the bot
bot.polling()


# Обработка call - запросы, при нажатии кнопки пользователем.
@bot.callback_query_handler(func=lambda call: button_handler)
def call_back(call):
    if call.message:
        global is_folder_delete

        if call.data == "Cоздать папку":
            global msg

            global mssg

            global choice_handler

            global UserDict

            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f"Введите название папки:  ")

            choice_handler = 2

        elif call.data == f"Переместить заметку":
            # Глобальная button_handler - для включения / выключения декоратора, отвечающего на call - запросы.
            global button_handler

            button_handler = False

            global CurrentFolder

            if len(UserDict[user_id].values()) >= 2:
                additional_keyboard = create_additional_keyboard(call.from_user.id)

                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=additional_keyboard,
                                            text="Введите название заметки, которую хотите переместить и папку,откуда переместить"
                                                 "и куда хотите переметить (пример: хлеб/фильмы/покупки): ")

                choice_handler = 3

            else:
                basic_keyboard = create_basic_keyboard(call.from_user.id)

                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=basic_keyboard,
                                            text="Перемещение невозможно/неправильно введенные данные: ")

                button_handler = True

        elif call.data == "Удалить папку":
            if len(UserDict[user_id]) >= 1:
                is_folder_delete = True

                optional_keyboard = create_optional_keyboard(call.from_user.id)

                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=optional_keyboard,
                                            text="Нажмите на папку, которую хотите удалить:")

            else:
                basic_keyboard = create_basic_keyboard(call.from_user.id)

                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text="Невозможно удалить несуществующие папки",
                                            reply_markup=basic_keyboard)
                button_handler = True

        elif call.data == "Удалить заметку":
            if count_notes >= 1:
                additional_keyboard = create_additional_keyboard(call.from_user.id)

                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=f"Введите название заметки, которую хотите удалить:",
                                            reply_markup=additional_keyboard)

                choice_handler = 5

            else:
                basic_keyboard = create_basic_keyboard(call.from_user.id)

                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text="Невозможно удалить несуществующие заметки",
                                            reply_markup=basic_keyboard)

        else:
            CurrentFolder = call.data

            if is_folder_delete == True:
                del UserDict[user_id][CurrentFolder]

                basic_keyboard = create_basic_keyboard(call.from_user.id)

                mssg = bot.send_message(call.message.chat.id, "Ваши папки, после удаления:",
                                        reply_markup=basic_keyboard)

                bot.delete_message(chat_id=call.message.chat.id, message_id=msg.message_id)

                is_folder_delete = False

            else:
                # Меняем значение choice_handler на 6.
                choice_handler = 6

                if len(UserDict[user_id][CurrentFolder]) < 1:
                    msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text=f"Выбранная папка {CurrentFolder}" + '\n' "Введите название заметки: ")

                else:
                    msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text=f"Выбранная папка {CurrentFolder}, в ней находится:"
                                                     f" {' '.join(UserDict[user_id][CurrentFolder])}"
                                                     + '\n'"Введите название заметки: ")


# Обработка текстовых сообщений от пользователя.
@bot.message_handler(content_types=["text"])
def add_note(message):
    # Сохранение текущего id пользователя.
    user_id = message.from_user.id

    # Глобальная choice_handler- для разграничения выбора функции при набирании текста пользователем.
    global choice_handler

    # Глобальная msg, в которой находится стартовое или последнее сообщение бота об итогах произведенного действия.
    global msg

    # Глобальная mssg, в которой находится cообщения, которые необходимо удалить при ошибке написания текста.
    global mssg

    # Глобальная button_handler - для включения / выключения декоратора, отвечающего на call - запросы.
    global button_handler

    global count_notes

    global is_folder_delete

    global UserDict

    if choice_handler == 1:
        bot.delete_message(chat_id=message.chat.id, message_id=mssg.message_id)

        basic_keyboard = create_basic_keyboard(message.from_user.id)

        mssg = bot.send_message(message.chat.id,
                                f'{message.from_user.username}, повторите попытку (нажмите кнопку папки для создания заметки,'
                                f' или кнопку с действием которое выхотите совершить).',
                                reply_markup=basic_keyboard)

        bot.delete_message(message.chat.id, message.message_id)

    elif choice_handler == 2:
        identical_folders = 0

        # Итерация всех названий папок. Проверка: не пытается ли пользователь создать идентичные папки.
        for name_folder in UserDict[message.from_user.id].keys():
            if name_folder == message.text:
                identical_folders = 1

        if identical_folders > 1:
            basic_keyboard = create_basic_keyboard(message.from_user.id)

            mssg = bot.send_message(message.chat.id, "Такая папка уже есть: ", reply_markup=basic_keyboard)

        else:
            UserDict[message.from_user.id][message.text] = list()

            # Открытие JSON-файла, для каждого пользователя отдельного, для хранения базы данных.
            with open(f"UserData/{message.from_user.id}.json", "w", encoding="utf-8") as write_file:
                json.dump(UserDict[user_id], write_file, ensure_ascii=False, indent=2, separators=(',', ': '))

            basic_keyboard = create_basic_keyboard(message.from_user.id)

            mssg = bot.send_message(message.chat.id, "Ваши папки:", reply_markup=basic_keyboard)

        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)

        bot.delete_message(message.chat.id, message.message_id)

        choice_handler = 1

        identical_folders = 0

    # Если пользователь нажал кнопку "переместить заметку" и произошла сменa choice_handler на 3.
    elif choice_handler == 3:
        moved_folders = 0

        if message.text.count(' ') == 2:
            for value in UserDict[user_id].values():
                message.text1, message.text2, message.text3 = message.text.split(' ')

                # Если заметка из сообщения имеется в значениях словаря, и ее нет в папке куда, надо переместить ее.
                if message.text1 in value and message.text1 not in UserDict[user_id][message.text3]:
                    UserDict[user_id][message.text2].remove(message.text1)

                    UserDict[user_id][message.text3].append(message.text1)

                    moved_folders = +1

                    if moved_folders >= 1:
                        additional_keyboard = create_additional_keyboard(message.from_user.id)

                        mssg = bot.send_message(message.chat.id, "Ваши заметки, после перемещения:",
                                                reply_markup=additional_keyboard)

                        break

                else:
                    additional_keyboard = create_additional_keyboard(message.from_user.id)

                    # Вывод текста, отражающего результат предыдущих действий (ошибка) и additional_keyboard.
                    mssg = bot.send_message(message.chat.id,
                                            "Перемещения не произошло, попробуйте заново"
                                            " (проверьте правильность написания/присутствие заметок):",
                                            reply_markup=additional_keyboard)

                    break

        else:
            additional_keyboard = create_additional_keyboard(message.from_user.id)

            # Вывод текста, отражающего результат предыдущих действий (ошибка) и additional_keyboard.
            mssg = bot.send_message(message.chat.id,
                                    "Перемещения не произошло, попробуйте заново"
                                    " (проверьте правильность написания/присутствие заметок):",
                                    reply_markup=additional_keyboard)

        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)

        bot.delete_message(message.chat.id, message.message_id)

        choice_handler = 1

        button_handler = True

        moved_folders = 0

    # Если пользователь нажал кнопку "удалить заметку" и произошла сменa choice_handler на 5.
    elif choice_handler == 5:
        deleted_notes = 0

        for value in UserDict[user_id].values():
            while message.text in value:
                value.remove(message.text)

                count_notes -= 1

                deleted_notes += 1

        if deleted_notes > 0:
            additional_keyboard = create_additional_keyboard(message.from_user.id)

            mssg = bot.send_message(message.chat.id, "Ваши заметки, после удаления:",
                                    reply_markup=additional_keyboard)

        else:
            additional_keyboard = create_additional_keyboard(message.from_user.id)

            mssg = bot.send_message(message.chat.id,
                                    "Заметки с таким именем не существует: проверьте написание):",
                                    reply_markup=additional_keyboard)

        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)

        bot.delete_message(message.chat.id, message.message_id)

        choice_handler = 1

    else:
        UserDict[user_id][CurrentFolder].append(message.text)

        # Открытие JSON-файла, для каждого пользователя отдельного, для хранения базы данных.
        with open(f"UserData/{message.from_user.id}.json", "w", encoding="utf-8") as write_file:
            json.dump(UserDict[user_id], write_file, ensure_ascii=False, indent=2, separators=(',', ': '))

        basic_keyboard = create_basic_keyboard(message.from_user.id)

        mssg = bot.send_message(message.chat.id,
                                text=f"Заметки из папки {CurrentFolder}: {' '.join(UserDict[user_id][CurrentFolder])}",
                                reply_markup=basic_keyboard)

        count_notes += 1

        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)

        bot.delete_message(message.chat.id, message.message_id)

        choice_handler = 1

if __name__ == "__main__":
    bot.polling(none_stop=True)