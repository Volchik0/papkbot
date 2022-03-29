from telegram.ext import Updater, Filters, MessageHandler, CallbackContext
from key import TOKEN
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from openpyxl import load_workbook
from connect_to_database import *


bd = load_workbook('base.xlsx')


def main():
    updater = Updater(
        token=TOKEN,
        use_context=True
    )

    dispatcher = updater.dispatcher

    keybord_handler = MessageHandler(Filters.text('клавиатура'), keybord)
    exo_handler = MessageHandler(Filters.all, exo)
    hallo_handler = MessageHandler(Filters.text('Привет, привет'), say_hallo)

    dispatcher.add_handler(hallo_handler)
    dispatcher.add_handler(keybord_handler)
    dispatcher.add_handler(exo_handler)

    updater.start_polling()
    updater.idle()


def say_hallo(update, context):
    name = update.message.from_user.first_name
    text = update.message.text
    update.message.reply_text(text="привет")


def exo(update: Update, context: CallbackContext):
    name = update.message.from_user.first_name
    user_id = update.message.chat_id
    text = update.message.text if update.message.text else "но текста нет"
    update.message.reply_text(text=f'Привет, {name}!\n'
                              f'Твой id: {user_id}\n'
                              f'Ты написал какой-то ****: {text}\n')


def keybord(update: Update, context: CallbackContext):
    buttons = [
        ['1', '2', '3'],
        ['привет', 'да', 'пока']
    ]
    keys = ReplyKeyboardMarkup
    update.message.reply_text(
        text='смотри, есть клава ',
        reply_markup=ReplyKeyboardMarkup(
            buttons,
            resize_keyboard=True

        )
    )


def meet(update: Update, context: CallbackContext):
    """
    Старт диалог по добавлению пользователя в БД.
    Будут собраны последовательно:
        имя
        пол
        класс
        id пользователя
    """
    user_id = update.message.from_user.id
    if in_database(user_id):
        pass  # выход из диадого
    ask_name(update, context)


def ask_name(update, Update, context: CallbackContext):
    """
    спашивает у пользователя имя
    TODO проверить имя пользователя в телеграме
    """
    update.message.reply_text(
        'ты не в базе данных\n'
        'введи своё имя'
    )


def ask_sex(update, Update, context: CallbackContext):
    """
    спашивает у пользователя пол
    """
    name = update.message.text
    context.user_data['name'] = name
    buttons = [
        ['М', 'Ж']
    ]
    keys = ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True
    )
    reply_text = f'приятно познакомится, {name}\n' + 'терепь введи свой пол'
    update.message.reply_text(
        reply_text,
        reply_markup=keys
    )

    def ask_grade(update, Update, context: CallbackContext):
        """
        спашивает у пользователя класс в котором он учится
        """
        sex = update.message.text
        context.user_data['name'] = sex
        buttons = [
            ['10н', '10о', '10н', '10о'],
            ['я не ученик']
        ]
        keys = ReplyKeyboardMarkup(
            buttons,
            resize_keyboard=True
        )
        reply_text = f''
        update.message.reply_text(
            reply_text,
            reply_markup=keys
        )


if __name__ == '__main__':
    main()
