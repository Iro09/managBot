from os import environ, path

from dotenv import load_dotenv

if path.exists("config.env"):
    load_dotenv("config.env")

BOT_TOKEN = environ.get("BOT_TOKEN", "5663640542:AAFZGOOICAB5xl7PPKWF7VFI1ZJJh3m773Y")
API_ID = int(environ.get("API_ID", "11796331"))
API_HASH = environ.get("API_HASH", "a089161b52f234bb90a6eb915551e8c0")
SUDO_USERS_ID = [int(x) for x in environ.get("SUDO_USERS_ID", "5518757491").split()]
LOG_GROUP_ID = int(environ.get("LOG_GROUP_ID", "-1001772857132"))
GBAN_LOG_GROUP_ID = int(environ.get("GBAN_LOG_GROUP_ID", "-1001772857132"))
MESSAGE_DUMP_CHAT = int(environ.get("MESSAGE_DUMP_CHAT", "-1001772857132"))
WELCOME_DELAY_KICK_SEC = int(environ.get("WELCOME_DELAY_KICK_SEC", "300"))
MONGO_URL = environ.get("MONGO_URL", "mongodb+srv://Gay:Gay@vickbhai.hief6ks.mongodb.net/?retryWrites=true&w=majority")
ARQ_API_URL = environ.get("ARQ_API_URL", "https://thearq.tech")
ARQ_API_KEY = environ.get("ARQ_API_KEY", "LIIHRD-ISXROY-VOVFUG-OVJWDL-ARQ")
RSS_DELAY = int(environ.get("RSS_DELAY", "300"))
UPSTREAM_REPO = environ.get(
    "UPSTREAM_REPO", "https://github.com/Lakshyaxdz/AnnuBot.git"
)
