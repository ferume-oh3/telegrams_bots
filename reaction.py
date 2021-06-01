import interaction
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from interaction import Queue, User, convert_to_route



bot = bot = telebot.TeleBot('1738728282:AAHfH-31hY0DXNlrPmb_JMv9Ao9Quzr5Jfo')
q = interaction.q


@bot.message_handler(commands=['start'])
def message_handler_st(message):
    print_all_messages()

    if not q.is_order(message.chat.id):
        bot.send_message(message.chat.id,
                         "Привет, я тестовый бот, попробую организовать функционал перевозки пассажиров "
                         "между городами. \nНе вижу у вас открытых заказов :) \nДля начала определимся водитель ли вы или пассажир?",
                         reply_markup=gen_markup_role())
    else:
        bot.send_message(message.chat.id,
                         "Рады вас снова видеть, хотите уточнить детали ваших поездок?",
                         reply_markup=gen_markup_check_order())

    print_all_messages()


@bot.message_handler(commands=['inform'])
def message_handler_inform(message):
    q.is_there(message.chat.id)
    print_all_messages()


@bot.message_handler(commands=['cancel'])
def message_handler_cancel(message):
    print_all_messages()
    if not q.is_order(message.chat.id):
        bot.send_message(message.chat.id, "Насколько нам известно у вас отсутсвуют активные заказы!")
    else:
        q.delete_order(message.chat.id)
        bot.send_message(message.chat.id, "Сделано!")

    print_all_messages()


@bot.message_handler(content_types=['text'])
def message_handler_any_message(message):
    print_all_messages()
    bot.send_message(message.chat.id,
                     "Я вас не понимаю! Используйте команду /start для начала работы или /inform для получения информации по вашему заказу или /cancel для отмены заказа!")


def print_all_messages():
    while q.is_there_message():
        mes = q.get_first_message()
        q.pop_first_message()
        bot.send_message(mes[1], mes[2])


def gen_markup_role():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Водитель", callback_data="cb_driver"),
               InlineKeyboardButton("Пассажир", callback_data="cb_passenger"))
    return markup


def gen_markup_order():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Уточнить", callback_data="cb_order"),
               InlineKeyboardButton("Нет спасибо", callback_data="cb_no_order"))
    return markup


def gen_markup_check_order():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Уточнить", callback_data="cb_order"),
               InlineKeyboardButton("Хочу отменить заказ", callback_data="cb_del_order"),
               InlineKeyboardButton("Нет спасибо", callback_data="cb_no_order"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_driver":
        add_driver(call)
        print_all_messages()
    elif call.data == "cb_passenger":
        add_passenger(call)
    elif call.data == "cb_order":
        check_order(call)
        print_all_messages()
    elif call.data == "cb_del_order":
        q.delete_order(call.message.chat.id)
        bot.answer_callback_query(call.id, "Сделано!")
        print_all_messages()
    elif call.data == "cb_no_order":
        bot.answer_callback_query(call.id, "Хорошо, приятного тыкания )")


def check_order(id):
    q.is_there(id)
    bot.answer_callback_query(id, "Готово")


def add_driver(call):
    bot.answer_callback_query(call.id, "Запомню")
    print_all_messages()
    msg = bot.send_message(call.message.chat.id, "Введите откуда и куда вы хотите ехать, например Казань Уфа")
    bot.register_next_step_handler(msg, new_order_driver)


def new_order_driver(message):
    q.add_driver(User(0, message.chat.id, convert_to_route(message.text)))
    print_all_messages()
    msg = bot.send_message(message.chat.id, "Ваш заказ зарегистрирован! Пожалуйста проверяйте статус заказа!")
    print_all_messages()


def add_passenger(call):
    bot.answer_callback_query(call.id, "Запомню")
    print_all_messages()
    msg = bot.send_message(call.message.chat.id, "Введите откуда и куда вы хотите ехать, например Казань Уфа")
    bot.register_next_step_handler(msg, new_order_passenger)


def new_order_passenger(message):
    q.add_passenger(User(1, message.chat.id, convert_to_route(message.text)))
    print_all_messages()
    msg = bot.send_message(message.chat.id, "Ваш заказ зарегистрирован! Пожалуйста проверяйте статус заказа!")
    print_all_messages()