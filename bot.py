import telebot
from telebot import types
import extensions
import config

print("bot.py запускается...")

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: types.Message):
    text = (
        "Привет! Я бот-конвертер валют.\n"
        "Чтобы узнать цену, отправь сообщение в формате:\n"
        "<валюта_исходная> <валюта_целевая> <количество>\n"
        "Примеры:\n"
        "евро рубль 10\n"
        "dollar euro 5\n\n"
        "Команды:\n"
        "/values — показать список доступных валют\n"
        "/help — показать это сообщение"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def list_values(message: types.Message):
    vals = set(extensions.CryptoConverter.VALUES.values())
    readable = '\n'.join(sorted(vals))
    bot.reply_to(message, f'Доступные валюты (ISO-коды):\n{readable}')


@bot.message_handler(content_types=['text'])
def convert_message(message: types.Message):
    text = message.text.strip()
    parts = text.split()

    if len(parts) != 3:
        bot.reply_to(message, 'Неверный формат. Ожидается: <валюта_from> <валюта_to> <количество>')
        return

    base, quote, amount = parts

    try:
        result = extensions.CryptoConverter.get_price(base, quote, amount)
    except extensions.APIException as e:
        bot.reply_to(message, f'Ошибка ({type(e).__name__}): {e}')
        return
    except Exception as e:
        bot.reply_to(message, f'Произошла непредвиденная ошибка ({type(e).__name__}): {e}')
        return

    try:
        amount_clean = float(amount.replace(',', '.'))
    except Exception:
        amount_clean = amount

    bot.reply_to(message, f'{amount_clean} {base} = {result} {quote}')



if __name__ == '__main__':
    print('Бот запущен... (Ctrl+C для остановки)')
    bot.infinity_polling()
