import reaction, telebot
from reaction import trip_bot

from interaction import Queue_of_orders


# def add_test(kek):
#     us[kek.id] = kek
#     st, fn = us[kek.id].start, us[kek.id].finish
#
#     if us[kek.id].role == 1:
#         if (st, fn) in orders_passengers:
#             orders_passengers[(st, fn)].append(kek)
#         else:
#             orders_passengers[(st, fn)] = [kek]
#     else:
#         if (st, fn) in orders_drivers:
#             orders_drivers[(st, fn)].append(kek)
#         else:
#             orders_drivers[(st, fn)] = [kek]


# add_test(user(1, 0, 'a', 'a', 1))
# add_test(user(1, 1, 'a', 'a', 1))
# add_test(user(1, 2, 'a', 'a', 1))
# add_test(user(1, 3, 'a', 'a', 1))

if __name__ == '__main__':
    q = Queue_of_orders({}, {}, {}, {}, [])
    bot = telebot.TeleBot()
    mine_bot = trip_bot(q, bot)
    mine_bot.bot_runner()