from datetime import date, datetime, time, timedelta
from typing import Dict

import pytz
import requests
from loguru import logger

from cbbi_bot.constants import (
    API_URL,
    BITCOIN_PRICE_KEY,
    CBBI_INDEX_KEY,
    LONG_PARAMETER_NAMES,
    USER_AGENT,
)


def get_cbbi_data() -> Dict[str, Dict[str, float]]:
    """Get JSON data from the API at colintalkscrypto.com/cbbi/data/latest.json.

    Returns:
        The CBBI data in a dictionary.

    """
    logger.info("Getting CBBI data...")

    return requests.get(API_URL, headers={"User-Agent": USER_AGENT}).json()


def get_todays_datetime() -> datetime:
    """Get a datetime object with today's date at midnight.

    Returns:
        A datetime object with today's date at midnight.

    """
    logger.debug("Getting datetime for today")

    today_date = date.today()
    midnight_here = datetime.combine(today_date, time())

    tz = pytz.timezone("UTC")
    return tz.localize(midnight_here)


def get_yesterdays_datetime() -> datetime:
    """Get a datetime object with yesterday's date at midnight.

    Returns:
        A datetime object with yesterday's date at midnight.

    """
    logger.debug("Getting datetime for yesterday")

    today_date = date.today()
    yesterday_date = today_date - timedelta(days=1)
    yesterday_midnight_here = datetime.combine(yesterday_date, time())

    tz = pytz.timezone("UTC")
    return tz.localize(yesterday_midnight_here)


def get_timestamp_from_datetime(dt: datetime) -> str:
    """Convert a datetime object to Unix timestamp string.

    Args:
        dt: The datetime to get the timestamp for.

    Returns:
        The timestamp in string format.

    """
    logger.debug("Getting timestamp from datetime")
    return str(int(dt.timestamp()))


def day_suffix(day: int) -> str:
    """Add a pretty print suffix to a day of the month.

    Args:
        day: The day of the month.

    Returns:
        A string with the day of the month and suffix (e.g. 5th).

    """
    logger.debug("Getting suffix for day of the month")
    if 11 <= day <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return suffix


def custom_strftime(format_: str, timestamp: datetime) -> str:
    """Pretty print a datetime object.

    Args:
        format_: The format to use.
        timestamp: The timestamp to convert.

    Returns:
        The formatted datetime as string.

    """
    logger.debug("Getting pretty date formatting")
    return timestamp.strftime(format_).replace(
        "{S}", str(timestamp.day) + day_suffix(timestamp.day)
    )


def get_emoji_dict(data: Dict[str, Dict[str, float]]) -> Dict[str, str]:
    """Create a dictionary of emojis showing whether a value has gone up,
        gone down, or stayed the same compared to yesterday.

    Args:
        data: The CBBI data to generate Emojis for.

    Returns:
        A dictionary with the CBBI metrics as keys, and the appropriate emojis
        as values.

    """
    logger.debug("Getting emoji dict")
    emoji_dict = {}
    today_ts = get_timestamp_from_datetime(get_todays_datetime())
    yesterday_ts = get_timestamp_from_datetime(get_yesterdays_datetime())
    for param in data.keys():
        if data[param][today_ts] > data[param][yesterday_ts]:
            emoji_dict[param] = "📈"
        elif data[param][today_ts] < data[param][yesterday_ts]:
            emoji_dict[param] = "📉"
        else:
            emoji_dict[param] = "〰️️"
    return emoji_dict


def get_full_metric_name(metric: str) -> str:
    """Get a longer name string for a CBBI metric.

    Args:
        metric: The metric to get the full name for.

    Returns:
        A string containing a longer version of the metric description.

    """
    logger.debug(f"Getting full metric name for metric {metric}")
    full_name = (
        LONG_PARAMETER_NAMES[metric]
        .replace(".", "\\.")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("-", "\\-")
    )
    return full_name


def get_message_header(
    data: Dict[str, Dict[str, float]], date_string: str, timestamp: str
):
    """Pretty format a message header line.

    Args:
        data: The CBBI data
        date_string: A pretty string for today's date
        timestamp: A timestamp string

    Returns:
        A nicely formatted header string.

    """
    logger.debug("Formatting message header line")

    cbbi_link = "[CBBI](https://cbbi.info/)"
    cbbi_today = float(data[CBBI_INDEX_KEY][timestamp])
    cbbi_warning = " ❗" if cbbi_today >= 0.9 else ""

    header_line = f"_{cbbi_link} update for {date_string}{cbbi_warning}_\n"

    return header_line


def get_message_cbbi(
    data: Dict[str, Dict[str, float]],
    emoji_dict: Dict[str, str],
    timestamp: str,
):
    """Pretty format a message line for the CBBI.

    Args:
        data: The CBBI data
        emoji_dict: Emoji dictionary indicating a metric's direction of change
        timestamp: A timestamp string

    Returns:
        A nicely formatted string for the CBBI.

    """
    logger.debug("Formatting message line for CBBI")

    cbbi_emoji = emoji_dict[CBBI_INDEX_KEY]
    cbbi_description = get_full_metric_name(CBBI_INDEX_KEY)
    cbbi_value = int(data[CBBI_INDEX_KEY][timestamp] * 100)

    cbbi_line = f"\n{cbbi_emoji} *{cbbi_description}: {cbbi_value}*\n"

    return cbbi_line


def get_message_price(
    data: Dict[str, Dict[str, float]],
    emoji_dict: Dict[str, str],
    timestamp: str,
):
    """Pretty format a message line for the Bitcoin price.

    Args:
        data: The CBBI data
        emoji_dict: Emoji dictionary indicating a metric's direction of change
        timestamp: A timestamp string

    Returns:
        A nicely formatted string for the Bitcoin price.

    """
    logger.debug("Formatting message line for Bitcoin price")

    price_emoji = emoji_dict[BITCOIN_PRICE_KEY]
    price_description = get_full_metric_name(BITCOIN_PRICE_KEY)
    price_value = data[BITCOIN_PRICE_KEY][timestamp]

    cbbi_line = f"\n{price_emoji} {price_description}: *${price_value:,.0f}*\n"

    return cbbi_line


def get_message_metric(
    data: Dict[str, Dict[str, float]],
    emoji_dict: Dict[str, str],
    metric: str,
    timestamp: str,
) -> str:
    """Pretty format a message line for a CBBI metric.

    Args:
        data: The CBBI data
        emoji_dict: Emoji dictionary indicating a metric's direction of change
        metric: The metric to generate a string for
        timestamp: A timestamp string

    Returns:
        A nicely formatted string for a particular metric.

    """
    logger.debug(f"Formatting message line for metric {metric}")

    if metric not in [CBBI_INDEX_KEY, BITCOIN_PRICE_KEY]:
        metric_value = data[metric][timestamp]
        metric_emoji = emoji_dict[metric]
        try:
            metric_desc = get_full_metric_name(metric)
            return f"\n{metric_emoji} {metric_desc}: *{metric_value:.0%}*"
        except KeyError:
            logger.warning(f"New metric {metric} found!")
            return f"\n{metric_emoji} {metric}: *{metric_value:.0%}* 🆕"

    else:
        return ""


def format_telegram_message(data: Dict[str, Dict[str, float]]) -> str:
    """Format the Telegram message to be sent to the chats.

    Args:
        data: The CBBI data.

    Returns:
        A formatted string message.

    """
    logger.info("Formatting Telegram message...")

    today_dt = get_todays_datetime()
    today_ts = get_timestamp_from_datetime(today_dt)
    pretty_date = custom_strftime("%B {S}, %Y", today_dt)

    emoji_dict = get_emoji_dict(data)

    message = get_message_header(data, pretty_date, today_ts)
    message += get_message_cbbi(data, emoji_dict, today_ts)
    message += get_message_price(data, emoji_dict, today_ts)
    for metric in data.keys():
        message += get_message_metric(data, emoji_dict, metric, today_ts)

    return message
