from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

CHAT_ID = env.int("CHAT_ID")
ip = env.str("ip")
CHANNEL_ID = env.int("CHANNEL_ID")

PG_USER = env.str("PG_USER")
PG_PASSWORD = env.str("PG_PASSWORD")
PG_NAME = env.str("PG_NAME")

POSTGRES_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{ip}/{PG_NAME}"
