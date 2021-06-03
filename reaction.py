import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import MatcherOfQueue, DriverPassengerClass
from MatcherOfQueue import MatcherOfQueue
from MessageClass import BotMessage
from DriverPassengerClass import Driver, Passenger


class TripBot():
    def __init__(self, Matcher, Bot):
        self.__Matcher = Matcher
        self.__Bot = Bot

    def PrintAllMessages(self):
        while self.__Matcher.IsThereMessage():
            Message = self.__Matcher.GetFirstMessage()
            self.__Matcher.PopFirstMessage()
            self.__Bot.send_message(Message.GetId(), Message.GetText())

    def CheckOrder(self, Call):
        self.__Matcher.GetInformationAboutOrder(Call.message.chat.id)
        self.__Bot.answer_callback_query(Call.id, "Готово")
        self.PrintAllMessages()

    def AddDriver(self, Call):
        self.__Bot.answer_callback_query(Call.id, "Запомню")
        self.PrintAllMessages()
        Message = self.__Bot.send_message(Call.message.chat.id, "Введите откуда и куда вы хотите ехать, например Казань Уфа")
        self.__Bot.register_next_step_handler(Message, self.NewOrderDriver)

    def NewOrderDriver(self, Message):
        self.__Matcher.AddDriver(Driver(Message.chat.id, ConverToRoute(Message.text)))
        self.PrintAllMessages()
        self.__Bot.send_message(Message.chat.id, "Ваш заказ зарегистрирован! Пожалуйста проверяйте статус заказа!")
        self.PrintAllMessages()

    def AddPassenger(self, Call):
        self.__Bot.answer_callback_query(Call.id, "Запомню")
        self.PrintAllMessages()
        Message = self.__Bot.send_message(Call.message.chat.id, "Введите откуда и куда вы хотите ехать, например Казань Уфа")
        self.__Bot.register_next_step_handler(Message, self.NewOrderPassenger)

    def NewOrderPassenger(self, Message):
        self.__Matcher.AddPassenger(Passenger(Message.chat.id, ConverToRoute(Message.text)))
        self.PrintAllMessages()
        self.__Bot.send_message(Message.chat.id, "Ваш заказ зарегистрирован! Пожалуйста проверяйте статус заказа!")
        self.PrintAllMessages()

    def BotRunner(self):
        @self.__Bot.message_handler(commands=['start'])
        def MessageHandlerStart(Message):
            self.PrintAllMessages()

            if not self.__Matcher.IsThereOrder(Message.chat.id):
                self.__Bot.send_message(Message.chat.id,
                                 "Привет, я тестовый бот, попробую организовать функционал перевозки пассажиров "
                                 "между городами. \nНе вижу у вас открытых заказов :) \nДля начала определимся водитель ли вы или пассажир?",
                                 reply_markup=GenMarkUpRole())
            else:
                self.__Bot.send_message(Message.chat.id,
                                 "Рады вас снова видеть, хотите уточнить детали ваших поездок?",
                                 reply_markup=GenMarkUpCheckOrder())

            self.PrintAllMessages()

        @self.__Bot.message_handler(commands=['inform'])
        def MessageHandlerInform(Message):
            self.__Matcher.GetInformationAboutOrder(Message.chat.id)
            self.PrintAllMessages()

        @self.__Bot.message_handler(commands=['cancel'])
        def MessageHandlerCancel(Message):
            self.PrintAllMessages()

            if not self.__Matcher.IsThereOrder(Message.chat.id):
                self.__Bot.send_message(Message.chat.id, "Насколько нам известно у вас отсутсвуют активные заказы!")
            else:
                self.__Matcher.DeleteOrder(Message.chat.id)
                self.__Bot.send_message(Message.chat.id, "Сделано!")

            self.PrintAllMessages()

        @self.__Bot.message_handler(content_types=['text'])
        def MessageHandlerOther(Message):
            self.PrintAllMessages()
            self.__Bot.send_message(Message.chat.id,
                             "Я вас не понимаю! Используйте команду /start для начала работы или /inform для получения информации по вашему заказу или /cancel для отмены заказа!")

        def GenMarkUpRole():
            Markup = InlineKeyboardMarkup()
            Markup.row_width = 2
            Markup.add(InlineKeyboardButton("Водитель", callback_data="cb_driver"),
                       InlineKeyboardButton("Пассажир", callback_data="cb_passenger"))
            return Markup

        def GenMarkUpCheckOrder():
            Markup = InlineKeyboardMarkup()
            Markup.row_width = 2
            Markup.add(InlineKeyboardButton("Уточнить", callback_data="cb_order"),
                       InlineKeyboardButton("Хочу отменить заказ", callback_data="cb_del_order"),
                       InlineKeyboardButton("Нет спасибо", callback_data="cb_no_order"))
            return Markup

        @self.__Bot.callback_query_handler(func=lambda call: True)
        def CallbackQuery(Call):
            if Call.data == "cb_driver":
                self.AddDriver(Call)
                self.PrintAllMessages()
            elif Call.data == "cb_passenger":
                self.AddPassenger(Call)
            elif Call.data == "cb_order":
                self.CheckOrder(Call)
                self.PrintAllMessages()
            elif Call.data == "cb_del_order":
                self.__Matcher.DeleteOrder(Call.message.chat.id)
                self.__Bot.answer_callback_query(Call.id, "Сделано!")
                self.PrintAllMessages()
            elif Call.data == "cb_no_order":
                self.__Bot.answer_callback_query(Call.id, "Хорошо, приятного тыкания )")

        self.__Bot.polling(none_stop=True, interval=0)


def ConverToRoute(Text):
    # add exception about len(text) != 2
    Text = Text.lower().split()
    Route = (Text[0], Text[1])
    return Route