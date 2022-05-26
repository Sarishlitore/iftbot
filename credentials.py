import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'credentials.env')
load_dotenv(dotenv_path)
bot_token = os.environ.get('BOT_TOKEN')
my_channel_id = os.environ.get('MY_CHANNEL_ID')
db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
