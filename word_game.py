import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = telebot.TeleBot('1738728282:AAHfH-31hY0DXNlrPmb_JMv9Ao9Quzr5Jfo')

checking = {'да', 'конечно', 'с удовольстием', 'давай', 'согласен', 'ладно', 'в бой', 'ну не знааааааю', 'погнали', 'окей', 'годно', 'я в деле'}
dic = []


@bot.message_handler(content_types=['text'])	
def start(message):
    if message.text.lower() == "привет":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Да', 'Нет', 'Бе')
        msg = bot.send_message(message.chat.id, "Привет, сыграем в игру?", reply_markup = markup)
        bot.register_next_step_handler(msg, initialize_game)
    elif message.text == "/help":
        bot.send_message(message.chat.id, "Напиши привет")
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю. Напиши /help.")


def initialize_game(message):
    global prev, dic
    
    if check(message.text):
        msg = bot.send_message(message.chat.id, "Ура!\nПравила следующие, мы играем в слова, я начну а ты продолжай!\nяблоко")
        dic = ['арбуз', 'банан', 'вишня', 'груша', 'дыня', 'ежевика', 'ёлка', 'желе', 'земляника', 'инжир', 'йогурт', 'киви', 'лимон', 'малина', 'нектарин', 'орех', 'пирожное', 'рябина', 'смородина', 'тыква', 'укроп', 'финик', 'хурма',
       'цветок', 'черника', 'шоколад', 'щука', 'ыаыаы', 'эскимо', 'юрта', 'ягода']
        bot.register_next_step_handler(msg, game)
        prev = 'яблоко'
    else:
        bot.send_message(message.chat.id, "Очень жаль : (")
	
def check(message):
    return (message.strip().lower() in checking)


def game(message):
    global prev
    
    if message.text[0] != prev[-1]:
        bot.send_message(message.chat.id, "Твое слово начинается не на последнюю букву моего!\nТы проиграл!")
    elif not check_word(message.text):
        bot.send_message(message.chat.id, "Мы используем только кирилицу!\nТы проиграл!")
    else:
        prev = find(message.text.lower())
        if len(prev) == 0:
            bot.send_message(message.chat.id, "А ты хорошь! Я проиграл!")
        else:
            msg = bot.send_message(message.chat.id, prev)
            bot.register_next_step_handler(msg, game)


def check_word(word):
    word = word.lower()
    for c in word:
        if not (c >= 'а' and c <= 'я'):
            return 0

    return 1


def find(word):
    for i in range(len(dic)):
        if dic[i][0] == word[-1]:
            s = dic[i]
            dic.pop(i)
            return s

    return ''

			
bot.polling(none_stop=True, interval=0)
