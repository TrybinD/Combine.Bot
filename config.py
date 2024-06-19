import os

from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.environ["BOT_TOKEN"]
ASYNC_CONNECTION_STRING = os.environ.get("ASYNC_CONNECTION_STRING", "sqlite+aiosqlite:///data/sqlite.db")
SYNC_CONNECTION_STRING = os.environ.get("SYNC_CONNECTION_STRING", "sqlite:///data/sqlite.db")
COMBINATOR_URL = os.environ.get("COMBINATOR_URL", "http://127.0.0.1:7000")
