import interaction
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from interaction import Queue_of_orders, User, convert_to_route


class trip_bot():
    def __init__(self, queue, bot):
        self.__queue = queue
        self.__bot = bot


    def print_all_messages(self):
        while self.__queue.is_there_message():
            mesage = self.__queue.get_first_message()
            self.__queue.pop_first_message()
            self.__bot.send_message(mesage[1], mesage[2])


    def check_order(self, call):
        self.__queue.is_there(call.message.chat.id)
        self.__bot.answer_callback_query(call.id, "Готово")


    def add_driver(self, call):
        self.__bot.answer_callback_query(call.id, "Запомню")
        self.print_all_messages()
        msg = self.__bot.send_message(call.message.chat.id, "Введите откуда и куда вы хотите ехать, например Казань Уфа")
        self.__bot.register_next_step_handler(msg, self.new_order_driver)


    def new_order_driver(self, message):
        self.__queue.add_driver(User(0, message.chat.id, convert_to_route(message.text)))
        self.print_all_messages()
        msg = self.__bot.send_message(message.chat.id, "Ваш заказ зарегистрирован! Пожалуйста проверяйте статус заказа!")
        self.print_all_messages()


    def add_passenger(self, call):
        self.__bot.answer_callback_query(call.id, "Запомню")
        self.print_all_messages()
        msg = self.__bot.send_message(call.message.chat.id, "Введите откуда и куда вы хотите ехать, например Казань Уфа")
        self.__bot.register_next_step_handler(msg, self.new_order_passenger)


    def new_order_passenger(self, message):
        self.__queue.add_passenger(User(1, message.chat.id, convert_to_route(message.text)))
        self.print_all_messages()
        msg = self.__bot.send_message(message.chat.id, "Ваш заказ зарегистрирован! Пожалуйста проверяйте статус заказа!")
        self.print_all_messages()


    def bot_runner(self):
        @self.__bot.message_handler(commands=['start'])
        def message_handler_st(message):
            self.print_all_messages()

            if not self.__queue.is_order(message.chat.id):
                self.__bot.send_message(message.chat.id,
                                 "Привет, я тестовый бот, попробую организовать функционал перевозки пассажиров "
                                 "между городами. \nНе вижу у вас открытых заказов :) \nДля начала определимся водитель ли вы или пассажир?",
                                 reply_markup=gen_markup_role())
            else:
                self.__bot.send_message(message.chat.id,
                                 "Рады вас снова видеть, хотите уточнить детали ваших поездок?",
                                 reply_markup=gen_markup_check_order())

            self.print_all_messages()


        @self.__bot.message_handler(commands=['inform'])
        def message_handler_inform(message):
            self.__queue.is_there(message.chat.id)
            self.print_all_messages()


        @self.__bot.message_handler(commands=['cancel'])
        def message_handler_cancel(message):
            self.print_all_messages()
            if not self.__queue.is_order(message.chat.id):
                self.__bot.send_message(message.chat.id, "Насколько нам известно у вас отсутсвуют активные заказы!")
            else:
                self.__queue.delete_order(message.chat.id)
                self.__bot.send_message(message.chat.id, "Сделано!")

            self.print_all_messages()


        @self.__bot.message_handler(content_types=['text'])
        def message_handler_any_message(message):
            self.print_all_messages()
            self.__bot.send_message(message.chat.id,
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


        @self.__bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            if call.data == "cb_driver":
                self.add_driver(call)
                self.print_all_messages()
            elif call.data == "cb_passenger":
                self.add_passenger(call)
            elif call.data == "cb_order":
                self.check_order(call)
                self.print_all_messages()
            elif call.data == "cb_del_order":
                self.__queue.delete_order(call.message.chat.id)
                self.__bot.answer_callback_query(call.id, "Сделано!")
                self.print_all_messages()
            elif call.data == "cb_no_order":
                self.__bot.answer_callback_query(call.id, "Хорошо, приятного тыкания )")


        self.__bot.polling(none_stop=True, interval=0)


