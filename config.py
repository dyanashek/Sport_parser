import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
BOT_ID = os.getenv('BOT_ID')
MANAGER_ID = os.getenv('MANAGER_ID')
USER_ID = os.getenv('USER_ID')

TABLE_TENNIS_URL = 'https://1xbet.com/LiveFeed/Get1x2_VZip?sports=10&count=1000&mode=4&country=180&getEmpty=true&noFilterBlockEvent=true'
LIVE_TABLE_TENNIS = 'https://1xbet.com/live/table-tennis/'

NOTIFY = True

ON_PAGE = 10