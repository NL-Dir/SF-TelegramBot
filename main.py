import json
import telebot
import requests
from config import TOKEN, API_KEY

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


@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    quote, base, amount = message.text.split(' ')
    r = requests.get(f'https://api.currencyapi.com/v3/latest?apikey={API_KEY}'
                     f'&currencies={keys[base]}&base_currency={keys[quote]}')
    total = float(json.loads(r.content)["data"][keys[base]]["value"])*float(amount)
    text = f'Цена {amount} {quote} в {base}: {total} '
    bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)
