import os
from dotenv import load_dotenv

load_dotenv()

# OpenWeatherMap API Key
JS_API_KEY = os.getenv("JS_API_KEY")

# jsonBin.io
JSONBIN_BIN_ID = os.getenv("JSONBIN_BIN_ID")
JSONBIN_API_KEY = os.getenv("JSONBIN_API_KEY")

GET_DETAILS_URL = os.getenv("GET_DETAILS_URL")
FIND_SEEDS_URL = os.getenv("FIND_SEEDS_URL")

HEADERS = {
    "X-Master-Key": JSONBIN_API_KEY
}
