import telebot
from config import TOKEN, keys
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


# имя бота @SF_pr_bot


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


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        user_request = message.text.split(' ')
        if len(user_request) > 3:
            raise APIException('Слишком много параметров.')
        quote, base, amount = user_request
        total = Converter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base}: {total} '
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)
