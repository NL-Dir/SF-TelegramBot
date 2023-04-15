import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
# имя бота @SF_pr_bot

keys = {
    'евро': 'EUR',
    'доллар': 'USD',
    'рубль': 'RUB'
}


@bot.message_handler(commands=['start', 'help'])
def bot_help(message: telebot.types.Message):
    text = 'Для начала работы введите запрос в следующем виде:\n <название валюты> <во что перевести> <сумма>\n \
Вывести все доступные валюты: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys:
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


bot.polling(non_stop=True)
