import interaction
from interaction import InlineKeyboardMarkup, InlineKeyboardButton, is_there, delete_order, add_driver, add_passenger, check_order

bot = interaction.bot
us = interaction.us
orders_passengers = interaction.orders_passengers
orders_drivers = interaction.orders_drivers
already_find = interaction.already_find


@bot.message_handler(commands=['start'])
def message_handler_st(message):
    if message.chat.id not in us:
        bot.send_message(message.chat.id,
                         "Привет, я тестовый бот, попробую организовать функционал перевозки пассажиров "
                         "между городами. \nНе вижу у вас открытых заказов :) \nДля начала определимся водитель ли вы или пассажир?",
                         reply_markup=gen_markup_role())
    else:
        bot.send_message(message.chat.id,
                         "Рады вас снова видеть, хотите уточнить детали ваших поездок?",
                         reply_markup=gen_markup_check_order())


@bot.message_handler(commands=['inform'])
def message_handler_inform(message):
    if message.chat.id not in us:
        log = (0, "Насколько нам известно у вас отсутсвуют активные заказы!")
    else:
        log = is_there((us[message.chat.id].start, us[message.chat.id].finish), message.chat.id)

    bot.send_message(message.chat.id, log[1])


@bot.message_handler(commands=['cancel'])
def message_handler_cancel(message):
    if message.chat.id not in us:
        bot.send_message(message.chat.id, "Насколько нам известно у вас отсутсвуют активные заказы!")
    else:
        delete_order(message)
        bot.send_message(message.chat.id, "Сделано!")


@bot.message_handler(content_types=['text'])
def message_handler_any_message(message):
    bot.send_message(message.chat.id,
                     "Я вас не понимаю! Используйте команду /start для начала работы или /inform для получения информации по вашему заказу или /cancel для отмены заказа!")


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
    elif call.data == "cb_passenger":
        add_passenger(call)
    elif call.data == "cb_order":
        check_order(call)
    elif call.data == "cb_del_order":
        delete_order(call.message)
        bot.answer_callback_query(call.id, "Сделано!")
    elif call.data == "cb_no_order":
        bot.answer_callback_query(call.id, "Хорошо, приятного тыкания )")
