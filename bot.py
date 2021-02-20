import os
from telegram.ext import Updater


INPUT_URL = 0


if __name__ == '__main__':

    updater = Updater(token=os.environ['TOKEN'], use_context=True)

    dp = updater.dispatcher
    updater.start_polling()
    updater.idle()
