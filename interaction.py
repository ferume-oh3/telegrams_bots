import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('1738728282:AAHfH-31hY0DXNlrPmb_JMv9Ao9Quzr5Jfo')

us = {}
orders_passengers = {}
orders_drivers = {}
already_find = {}


class user():
    def __init__(self, role, id, start, finish):
        self.id = id
        self.role = role
        self.start = start
        self.finish = finish


def convert_to_route(text):
    # add exception about len(text) != 2
    text = text.lower().split()
    route = (text[0], text[1])
    return route


def add_driver(call):
    us[call.message.chat.id] = user(0, call.message.chat.id, "венера", "юпитер")
    bot.answer_callback_query(call.id, "Запомню")
    msg = bot.send_message(call.message.chat.id, "Введите откуда и куда вы хотите ехать, например Казань Уфа")
    bot.register_next_step_handler(msg, new_order_driver)


def new_order_driver(message):
    msg = bot.send_message(message.chat.id, "Ваш заказ зарегистрирован! Пожалуйста проверяйте статус заказа!")
    st, fn = convert_to_route(message.text)
    us[message.chat.id].start = st
    us[message.chat.id].finish = fn
    if (st, fn) in orders_drivers:
        orders_drivers[(st, fn)].append(us[message.chat.id])
    else:
        orders_drivers[(st, fn)] = [us[message.chat.id]]

    while may_build_trip((st, fn)):
        build_trip((st, fn))


def add_passenger(call):
    us[call.message.chat.id] = user(1, call.message.chat.id, "юпитер", "венера")
    bot.answer_callback_query(call.id, "Запомню")
    msg = bot.send_message(call.message.chat.id, "Введите откуда и куда вы хотите ехать, например Казань Уфа")
    bot.register_next_step_handler(msg, new_order_passenger)


def new_order_passenger(message):
    msg = bot.send_message(message.chat.id, "Ваш заказ зарегистрирован! Пожалуйста проверяйте статус заказа!")
    st, fn = convert_to_route(message.text)
    us[message.chat.id].start = st
    us[message.chat.id].finish = fn
    if (st, fn) in orders_passengers:
        orders_passengers[(st, fn)].append(us[message.chat.id])
    else:
        orders_passengers[(st, fn)] = [us[message.chat.id]]

    while may_build_trip((st, fn)):
        build_trip((st, fn))


def check_order(call):
    log = is_there((us[call.message.chat.id].start, us[call.message.chat.id].finish), call.message.chat.id)
    bot.answer_callback_query(call.id, log[1])


def is_there(route, id):
    if id in already_find:
        return (1, get_inform(id))

    if route not in orders_drivers or len(orders_drivers[route]) == 0:
        return (0, "К сожалению водитель пока не нашелся : (")
    elif route not in orders_passengers:
        return (0, "Недостаточно пассажиров, осталось найти 4")
    elif len(orders_passengers[route]) != 4:
        return (0, "Недостаточно пассажиров, осталось найти " + str(4 - len(orders_passengers[route])))
    else:
        assert (0)


def get_inform(id):
    if us[id].role == 0:
        return "Все пассажиры нашлись, ниже приложены их номера\n" + '\n'.join(list(map(str, already_find[id])))
    else:
        return "Водитель нашелся, ниже приложен его номер\n" + '\n'.join(list(map(str, already_find[id])))


def delete_order(message):
    id = message.chat.id
    route = (us[id].start, us[id].finish)

    if us[id].role == 0:
        if id in already_find:
            inform_about_delete_of_driver(already_find[id])

            for id_pas in already_find[id]:
                orders_passengers[route].append(us[id_pas])
                already_find.pop(id_pas, None)

            already_find.pop(id, None)
            us.pop(id, None)
        else:
            orders_drivers[route].pop(orders_drivers[route].index(us[id]))
            us.pop(id, None)
    else:
        if id in already_find:
            fl = already_find[already_find[id][0]][::]
            fl.pop(fl.index(id))
            fl.append(already_find[id][0])
            inform_about_delete_of_passenger(fl)

            id_dr = already_find[id][0]
            for id_pas in already_find[id_dr]:
                if id_pas != id:
                    orders_passengers[route].append(us[id_pas])

                already_find.pop(id_pas, None)

            already_find.pop(id_dr, None)
            orders_drivers[route].append(us[id_dr])
            us.pop(id, None)
        else:
            orders_passengers[route].pop(orders_passengers[route].index(us[id]))
            us.pop(id, None)

    while may_build_trip(route):
        build_trip(route)


def inform_about_delete_of_driver(whom):
    for v in whom:
        if not us[v].label_test:
            bot.send_message(v, "Водитель отказался от поездки, ищем нового")


def inform_about_delete_of_passenger(whom):
    for v in whom:
        if not us[v].label_test:
            bot.send_message(v, "Один из пассажиров отказался от поездки, ищем нового")


def may_build_trip(route):
    if route not in orders_drivers or route not in orders_passengers:
        return 0

    return len(orders_drivers[route]) >= 1 and len(orders_passengers[route]) >= 4


def build_trip(route):
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

    already_find[dr] = [ps1, ps2, ps3, ps4]
    already_find[ps1] = already_find[ps2] = already_find[ps3] = already_find[ps4] = [dr]

    if not us[dr].label_test:
        bot.send_message(dr, "Все пассажиры нашлись, ниже приложены их номера\n" + '\n'.join(
            list(map(str, already_find[dr]))))

    for v in already_find[dr]:
        if not us[v].label_test:
            bot.send_message(v,
                             "Водитель нашелся, ниже приложен его номер\n" + '\n'.join(list(map(str, already_find[v]))))


def add_test(kek):
    us[kek.id] = kek
    st, fn = us[kek.id].start, us[kek.id].finish

    if us[kek.id].role == 1:
        if (st, fn) in orders_passengers:
            orders_passengers[(st, fn)].append(kek)
        else:
            orders_passengers[(st, fn)] = [kek]
    else:
        if (st, fn) in orders_drivers:
            orders_drivers[(st, fn)].append(kek)
        else:
            orders_drivers[(st, fn)] = [kek]