import reaction, telebot, QueueOfPassengers, QueueOfDrivers
from reaction import TripBot

from MatcherOfQueue import MatcherOfQueue
from QueueOfDrivers import QueueOfDriver
from QueueOfPassengers import QueueOfPassenger


if __name__ == '__main__':
    Matcher = MatcherOfQueue(QueueOfDriver({}, {}), QueueOfPassenger({}, {}), {}, [])
    Bot = telebot.TeleBot('1738728282:AAHfH-31hY0DXNlrPmb_JMv9Ao9Quzr5Jfo')
    MineBot = TripBot(Matcher, Bot)
    MineBot.BotRunner()