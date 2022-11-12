from os import environ, path

from dotenv import load_dotenv

if path.exists("config.env"):
    load_dotenv("config.env")

BOT_TOKEN = environ.get("BOT_TOKEN", "5694028061:AAHlS1BqmOFk6IGEJQp_pPYiZgZFHuSDAO4")
API_ID = int(environ.get("API_ID", "23315924"))
API_HASH = environ.get("API_HASH", "3b39bf8e305df7b2f310ce6f53392ac6")
SUDO_USERS_ID = [int(x) for x in environ.get("SUDO_USERS_ID", "5722601919").split()]
LOG_GROUP_ID = int(environ.get("LOG_GROUP_ID", "-1001848895379"))
GBAN_LOG_GROUP_ID = int(environ.get("GBAN_LOG_GROUP_ID", "-1001848895379"))
MESSAGE_DUMP_CHAT = int(environ.get("MESSAGE_DUMP_CHAT", "-1001616008828"))
WELCOME_DELAY_KICK_SEC = int(environ.get("WELCOME_DELAY_KICK_SEC", "300"))
MONGO_URL = environ.get("MONGO_URL", "mongodb+srv://deadterabaap09:dead@cluster0.3a4z5gq.mongodb.net/?retryWrites=true&w=majority")
ARQ_API_URL = environ.get("ARQ_API_URL", "https://thearq.tech")
ARQ_API_KEY = environ.get("ARQ_API_KEY", "LIIHRD-ISXROY-VOVFUG-OVJWDL-ARQ")
RSS_DELAY = int(environ.get("RSS_DELAY", "300"))
UPSTREAM_REPO = environ.get(
    "UPSTREAM_REPO", "https://github.com/rozari0/NezukoBot.git"
)
