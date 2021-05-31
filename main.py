import reaction

bot = reaction.bot

# add_test(user(1, 0, 'a', 'a', 1))
# add_test(user(1, 1, 'a', 'a', 1))
# add_test(user(1, 2, 'a', 'a', 1))
# add_test(user(1, 3, 'a', 'a', 1))

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
