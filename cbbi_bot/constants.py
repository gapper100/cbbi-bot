import os

API_URL = "https://colintalkscrypto.com/cbbi/data/latest.json"
USER_AGENT = (
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"
)

PRIVATE_CHAT_ID = os.environ["TELEGRAM_CRYPTO_CHAT_ID"]
CHANNEL_CHAT_ID = os.environ["TELEGRAM_CBBI_CHANNEL_ID"]

TOKEN = os.environ["TELEGRAM_TOKEN"]

CBBI_INDEX_KEY = "Confidence"
BITCOIN_PRICE_KEY = "Price"

METRICS = [
    "GoldenRatio",
    "GoogleTrends",
    "StockToFlow",
    "PiCycle",
    "2YMA",
    "Trolololo",
    "RUPL",
    "Puell",
    "MVRV",
    "RHODL",
    "ReserveRisk",
]

LONG_PARAMETER_NAMES = {
    "Confidence": "CBBI",
    "Price": "Bitcoin price",
    "GoldenRatio": "The Golden 51%-49% Ratio",
    "GoogleTrends": '"Bitcoin" Google search term',
    "StockToFlow": "Stock-To-Flow Chart",
    "PiCycle": "Pi Cycle Top Indicator",
    "2YMA": "2 Year Moving Average",
    "Trolololo": "Bitcoin Trolololo Trend Line",
    "RUPL": "RUPL/NUPL Chart",
    "Puell": "Puell Multiple",
    "MVRV": "MVRV Z-score",
    "RHODL": "RHODL Ratio",
    "ReserveRisk": "Reserve Risk",
}
