import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = telebot.TeleBot('1738728282:AAHfH-31hY0DXNlrPmb_JMv9Ao9Quzr5Jfo')
role = {}
orders = {}
orders_passengers = {}
orders_drivers = {}


def information(message):
    if message.chat.id in role and role[message.chat.id] == 0 and message.chat.id in orders_drivers:
        return len(orders[orders_drivers[message.chat.id]])
    elif message.chat.id in role and role[message.chat.id] == 1 and message.chat.id in orders_passengers:
        return len(orders[passenger_order[message.chat.id]])
    else:
        return -1


def retype_to_string(cnt):
    if cnt != -1:
        return "Осталось найти " + str(5 - cnt) + " пассажиров и поедем!"
    else:
        return "Мы все потеряли!"


@bot.message_handler(commands=['start'])
def message_handler_st(message):
    if message.chat.id not in role:
        bot.send_message(message.chat.id, "Привет, я тестовый бот, попробую организовать функционал перевозки пассажиров "
                                      "между городами. \nНе вижу у вас открытых заказов :) \nДля начала определимся водитель ли вы или пассажир?", reply_markup=gen_markup_role())
    else:
        bot.send_message(message.chat.id,
                         "Рады вас снова видеть, хотите уточнить детали ваших поездок?",
                         reply_markup=gen_markup_check_order())


@bot.message_handler(commands=['inform'])
def message_handler_inf(message):
    bot.send_message(message.chat.id, retype_to_string(information(message)))


@bot.message_handler(content_types=['text'])
def message_handler_bla(message):
    bot.send_message(message.chat.id, "Я вас не понимаю! Используйте команду /start для начала работы или /inform для получения информации по вашему заказу!")

def message_handler(message):
    information(message)


@bot.message_handler(commands=['information'])
def message_handler(message):
    information(message)


@bot.message_handler(content_types=['text'])
def message_handler(message):
    bot.send_message(message.chat.id, "Я вас не понимаю, воспользуйтесь, пожалуйста командой  /start")


def gen_markup_role():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Водитель", callback_data="cb_driver"), InlineKeyboardButton("Пассажир", callback_data="cb_passenger"))
    return markup


def gen_markup_order():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Уточнить", callback_data="cb_order"), InlineKeyboardButton("Нет спасибо", callback_data="cb_no_order"))
    return markup


def gen_markup_check_order():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Уточнить", callback_data="cb_order"), InlineKeyboardButton("Нет спасибо", callback_data="cb_no_order"))
    return markup


def new_order_passenger(message):
    if message.text.lower() not in orders:
        msg = bot.send_message(message.chat.id, "Простите, мы не можем зарегистрировать заказ, ни один водитель не берется...")
        role.pop(message.chat.id, None)
    else:
        msg = bot.send_message(message.chat.id, "Ваш заказ зарегистрирован! Пожалуйста проверяйте статус заказа!")
        orders[message.text.lower()].append(message.chat.id)
        orders_passengers[message.chat.id] = message.text.lower()


def new_order_driver(message):
    msg = bot.send_message(message.chat.id, "Ваш заказ зарегистрирован! Пожалуйста проверяйте статус заказа!")
    orders[message.text.lower()] = [message.chat.id]
    orders_drivers[message.chat.id] = message.text.lower()


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_driver":
        role[call.message.chat.id] = 0
        bot.answer_callback_query(call.id, "Запомню")
        msg = bot.send_message(call.message.chat.id, "Введите откуда и куда вы хотите ехать, например Казань Уфа")
        bot.register_next_step_handler(msg, new_order_driver)
    elif call.data == "cb_passenger":
        role[call.message.chat.id] = 1
        bot.answer_callback_query(call.id, "Запомню")
        msg = bot.send_message(call.message.chat.id, "Введите откуда и куда вы хотите ехать, например Казань Уфа")
        bot.register_next_step_handler(msg, new_order_passenger)
    elif call.data == "cb_order":
        inform = retype_to_string(information(call.message))
        bot.answer_callback_query(call.id, inform)
    elif call.data == "cb_no_order":
        bot.answer_callback_query(call.id, "Хорошо, приятного тыкания )")

			
bot.polling(none_stop=True, interval=0)
