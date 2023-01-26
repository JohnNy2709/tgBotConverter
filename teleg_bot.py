import telebot
from extensions import Converter, APIException
from config import Token, keys


bot = telebot.TeleBot(Token)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = """Чтобы начать работу, введите команду следующего вида:
<название валюты> <название валюты, в которую необходимо конвертировать> \
<количество конвертируемой валюты>
\nПосмотреть доступные валюты: /values
"""
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def handle_values(message):
    text = 'Доступные валюты:'
    for key in keys:
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message:telebot.telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
                raise APIException('Неверное количество параметров.')
        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось выполнить команду.\n{e}')
    else:
        text=f'Стоимость {amount} {quote} в {base}:\n{total_base}'
        bot.reply_to(message, text)

bot.polling(none_stop=True)