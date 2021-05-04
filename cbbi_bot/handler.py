import telegram
from constants import TOKEN, PRIVATE_CHAT_ID, CHANNEL_CHAT_ID
from functions import get_cbbi_data, format_telegram_message


def send_message(event=None, context=None):
    data = get_cbbi_data()
    message = format_telegram_message(data)

    bot = telegram.Bot(token=TOKEN)
    bot.sendMessage(chat_id=PRIVATE_CHAT_ID, text=message, parse_mode='MarkdownV2')
    bot.sendMessage(chat_id=CHANNEL_CHAT_ID, text=message, parse_mode='MarkdownV2')


if __name__ == '__main__':
    send_message()
