import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = telebot.TeleBot('1738728282:AAHfH-31hY0DXNlrPmb_JMv9Ao9Quzr5Jfo')
us = {}

orders_passengers = {}
orders_drivers = {}
finding_right = {}


class user():
    def __init__(self, role, id, start, finish):
        self.id = id
        self.role = role
        self.start = start
        self.finish = finish


@bot.message_handler(commands=['start'])
def message_handler_st(message):
    if message.chat.id not in us:
        bot.send_message(message.chat.id, "Привет, я тестовый бот, попробую организовать функционал перевозки пассажиров "
                                      "между городами. \nНе вижу у вас открытых заказов :) \nДля начала определимся водитель ли вы или пассажир?", reply_markup=gen_markup_role())
    else:
        bot.send_message(message.chat.id,
                         "Рады вас снова видеть, хотите уточнить детали ваших поездок?",
                         reply_markup=gen_markup_check_order())


@bot.message_handler(commands=['inform'])
def message_handler_inf(message):
	if message.chat.id not in us:
		log = (0, "Насколько нам известно у вас отсутсвуют активные заказы!")
	else:
		log = is_there((us[message.chat.id].start, us[message.chat.id].finish), message.chat.id)
	
	bot.send_message(message.chat.id, log[1])
	if log[0]:
		build_trip((us[message.chat.id].start, us[message.chat.id].finish), message)



@bot.message_handler(content_types=['text'])
def message_handler_bla(message):
    bot.send_message(message.chat.id, "Я вас не понимаю! Используйте команду /start для начала работы или /inform для получения информации по вашему заказу!")

def message_handler(message):
    information(message)


@bot.message_handler(commands=['information'])
def message_handler(message):
    information(message)


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
    markup.add(InlineKeyboardButton("Уточнить", callback_data="cb_order"), InlineKeyboardButton("Хочу отменить заказ", callback_data="cb_del_order"), InlineKeyboardButton("Нет спасибо", callback_data="cb_no_order"))
    return markup


def new_order_passenger(message):
    msg = bot.send_message(message.chat.id, "Ваш заказ зарегистрирован! Пожалуйста проверяйте статус заказа!")
    st, fn = convert_to_route(message.text)
    us[message.chat.id].start = st
    us[message.chat.id].finish = fn
    if (st, fn) in orders_passengers:
    	orders_passengers[(st, fn)].append(us[message.chat.id])
    else:
    	orders_passengers[(st, fn)] = [us[message.chat.id]]


def new_order_driver(message):
    msg = bot.send_message(message.chat.id, "Ваш заказ зарегистрирован! Пожалуйста проверяйте статус заказа!")
    st, fn = convert_to_route(message.text)
    us[message.chat.id].start = st
    us[message.chat.id].finish = fn
    if (st, fn) in orders_drivers:
    	orders_drivers[(st, fn)].append(us[message.chat.id])
    else:
    	orders_drivers[(st, fn)] = [us[message.chat.id]]


def is_there(route, id):
	if id in finding_right:
		return (1, "Поездка состоится!")

	if route not in orders_drivers:
		return (0, "К сожалению водитель пока не нашелся : (")
	elif route not in orders_passengers:
		return (0, "Недостаточно пассажиров, осталось найти 4")
	elif len(orders_passengers[route]) != 4:
		return (0, "Недостаточно пассажиров, осталось найти " + str(4 - len(orders_passengers[route])))
	else:
		return (1, "Поездка состоится, ура!")


def convert_to_route(text):
	text = text.lower().split()
	route = (text[0], text[1])
	return route



def build_trip(route, message):
	if message.chat.id in finding_right:
		msg = bot.send_message(call.message.chat.id, "Необходимые контакты:\n" + '\n'.join(map(str, finding_right[message.chat.id])))
		finding_right.pop(message.chat.id, None)
		us.pop(message.chat.id, None)
	else:	
		dr = orders_drivers[route][0].id
		orders_drivers[route].pop(0)
		ps1 = orders_passengers[route][0].id
		orders_passengers[route].pop(0)
		ps2 = orders_passengers[route][0].id
		orders_passengers[route].pop(0)
		ps3 = orders_passengers[route][0].id
		orders_passengers[route].pop(0)
		ps4 = orders_passengers[route][0].id
		orders_passengers[route].pop(0)

		finding_right[dr] = [ps1, ps2, ps3, ps4]
		finding_right[ps1] = finding_right[ps2] = finding_right[ps3] = finding_right[ps4] = [dr]



def add_driver(call):
    us[call.message.chat.id] = user(0, call.message.chat.id, "венера", "юпитер")
    bot.answer_callback_query(call.id, "Запомню")
    msg = bot.send_message(call.message.chat.id, "Введите откуда и куда вы хотите ехать, например Казань Уфа")
    bot.register_next_step_handler(msg, new_order_driver)


def add_passenger(call):
    us[call.message.chat.id] = user(1, call.message.chat.id, "юпитер", "венера")
    bot.answer_callback_query(call.id, "Запомню")
    msg = bot.send_message(call.message.chat.id, "Введите откуда и куда вы хотите ехать, например Казань Уфа")
    bot.register_next_step_handler(msg, new_order_passenger)


def check_order(call):
    log = is_there((us[call.message.chat.id].start, us[call.message.chat.id].finish), call.message.chat.id)
    bot.answer_callback_query(call.id, log[1])
    if log[0]:
    	build_trip((us[call.message.chat.id].start, us[call.message.chat.id].finish), call.message)


def delete_order(call):
	id = call.message.chat.id
	route = (us[id].start, us[id].finish)

	if us[id].role == 0:
		if id in finding_right:
			for id_pas in finding_right[id]:
				orders_passengers[route].append(us[id_pas])
				finding_right.pop(id_pas, None)

			finding_right.pop(id, None)
			us.pop(id, None)
		else:
			orders_drivers[route].pop(orders_drivers[route].index(us[id]))
			us.pop(id, None)
	else:
		if id in finding_right:
			id_dr = finding_right[id]
			
			for id_pas in finding_right[id]:
				if id_pas != id:
					orders_passengers[route].append(us[id_pas])
				
				finding_right.pop(id_pas, None)


			finding_right.pop(id_dr, None)
			orders_drivers[route].append(us[id_dr])
			us.pop(id, None)
		else:
			orders_passengers[route].pop(orders_passengers[route].index(us[id]))
			us.pop(id, None)

	bot.answer_callback_query(call.id, "Сделано!")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_driver":
    	add_driver(call)
    elif call.data == "cb_passenger":
        add_passenger(call)
    elif call.data == "cb_order":
    	check_order(call)
    elif call.data == "cb_del_order":
    	delete_order(call)
    elif call.data == "cb_no_order":
        bot.answer_callback_query(call.id, "Хорошо, приятного тыкания )")

			
bot.polling(none_stop=True, interval=0)
