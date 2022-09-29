import telebot
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def handle_start_help(message):

    bot.send_message(
        message.chat.id, 'Добро пожаловать в автоматизированный журнал событий команды Потенциал')


bot.polling(none_stop=True)
