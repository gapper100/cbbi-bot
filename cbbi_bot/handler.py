import telegram
from constants import CHANNEL_CHAT_ID, PRIVATE_CHAT_ID, TOKEN
from functions import format_telegram_message, get_cbbi_data
from loguru import logger


def send_message(event=None, context=None) -> None:
    """Send a CBBI update to Telegram chats.

    Args:
        event: A Telegram Event object.
        context: A Telegram Context object.

    """
    logger.info("Sending daily CBBI update!")
    data = get_cbbi_data()
    message = format_telegram_message(data)
    bot = telegram.Bot(token=TOKEN)

    logger.info("Sending message to group...")
    bot.sendMessage(chat_id=PRIVATE_CHAT_ID, text=message, parse_mode="MarkdownV2")

    logger.info("Sending message to channel...")
    bot.sendMessage(chat_id=CHANNEL_CHAT_ID, text=message, parse_mode="MarkdownV2")


if __name__ == "__main__":
    send_message()
