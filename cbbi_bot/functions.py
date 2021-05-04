from datetime import date, datetime, time, timedelta

import pytz
import requests
from constants import (
    API_URL,
    BITCOIN_PRICE_KEY,
    CBBI_INDEX_KEY,
    LONG_PARAMETER_NAMES,
    METRICS,
    USER_AGENT,
)
from loguru import logger


def get_cbbi_data() -> dict[str, dict[str, float]]:
    logger.info("Getting CBBI data...")

    return requests.get(API_URL, headers={"User-Agent": USER_AGENT}).json()


def get_todays_datetime() -> datetime:
    logger.debug("Getting datetime for today")

    today_date = date.today()
    midnight_here = datetime.combine(today_date, time())

    tz = pytz.timezone("UTC")
    return tz.localize(midnight_here)


def get_yesterdays_datetime() -> datetime:
    logger.debug("Getting datetime for yesterday")

    today_date = date.today()
    yesterday_date = today_date - timedelta(days=1)
    yesterday_midnight_here = datetime.combine(yesterday_date, time())

    tz = pytz.timezone("UTC")
    return tz.localize(yesterday_midnight_here)


def get_timestamp_from_datetime(dt: datetime) -> str:

    logger.debug("Getting timestamp from datetime")
    return str(int(dt.timestamp()))


def day_suffix(day: int) -> str:

    logger.debug("Getting suffix for day of the month")
    return "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")


def custom_strftime(format_: str, timestamp: datetime) -> str:

    logger.debug("Getting pretty date formatting")
    return timestamp.strftime(format_).replace(
        "{S}", str(timestamp.day) + day_suffix(timestamp.day)
    )


def get_emoji_dict(data: dict[str, dict[str, float]]) -> dict[str, str]:
    logger.debug("Getting emoji dict")
    emoji_dict = {}
    today_timestamp = get_timestamp_from_datetime(get_todays_datetime())
    yesterday_timestamp = get_timestamp_from_datetime(get_yesterdays_datetime())
    for param in data.keys():
        if data[param][today_timestamp] > data[param][yesterday_timestamp]:
            emoji_dict[param] = "📈"
        elif data[param][today_timestamp] < data[param][yesterday_timestamp]:
            emoji_dict[param] = "📉"
        else:
            emoji_dict[param] = "〰️️"
    return emoji_dict


def get_full_metric_name(metric: str) -> str:
    logger.debug(f"Getting full metric name for metric {metric}")
    full_name = (
        LONG_PARAMETER_NAMES[metric]
        .replace(".", "\\.")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("-", "\\-")
    )
    return full_name


def format_metric_message(
    data: dict[str, dict[str, float]],
    emoji_dict: dict[str, str],
    metric: str,
    today_timestamp: str,
) -> str:
    logger.debug(f"Formatting message line for metric {metric}")
    return (
        f"\n{emoji_dict[metric]} {get_full_metric_name(metric)}: "
        f"*{data[metric][today_timestamp]:.0%}*"
    )


def format_telegram_message(data: dict[str, dict[str, float]]) -> str:
    logger.info("Formatting Telegram message...")
    today_dt = get_todays_datetime()
    pretty_date_string = custom_strftime("%B {S}, %Y", today_dt)
    today_timestamp = get_timestamp_from_datetime(today_dt)

    emoji_dict = get_emoji_dict(data)

    cbbi_warning = " ❗" if float(data[CBBI_INDEX_KEY][today_timestamp]) >= 0.9 else ""

    message = f"""_[CBBI](https://cbbi.info/) update for {pretty_date_string}{cbbi_warning}_\n
{emoji_dict[CBBI_INDEX_KEY]} *{get_full_metric_name(CBBI_INDEX_KEY)}: {int(data[CBBI_INDEX_KEY][today_timestamp]*100)}*\n
{emoji_dict[BITCOIN_PRICE_KEY]} {get_full_metric_name(BITCOIN_PRICE_KEY)}: *${data[BITCOIN_PRICE_KEY][today_timestamp]:,.0f}*\n"""

    for metric in METRICS:
        message += format_metric_message(data, emoji_dict, metric, today_timestamp)

    return message