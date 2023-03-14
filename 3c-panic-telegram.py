import telegram
from colorama import Fore
from telegram.ext import *
from py3cw.request import Py3CW
import time

z = """
  ___________                  _        
 |___  / ____|                | |       
    / / |     _ __ _   _ _ __ | |_ ___  
   / /| |    | '__| | | | '_ \| __/ _ \ 
  / /_| |____| |  | |_| | |_) | || (_) |
 /_____\_____|_|   \__, | .__/ \__\___/ 
                    __/ | |             
                   |___/|_|             
"""
##############################################################################################
# Telegram bot
allowed = 1539032943 # your telegram user id
sorry = "Sorry !.\n Who are you ?!\n"
telegram_api = ""  # your telegram bot token

# 3Commas details
p3cw = Py3CW(
    key='',  # replace your API key here
    secret='', # replace your API secret here
    request_options={
        'request_timeout': 10,
        'nr_of_retries': 1,
        'retry_status_codes': [502],
        'retry_backoff_factor': 0.1
    }
)


def get_close_deals():
    bots_ids = []
    error, data = p3cw.request(
        entity="bots",
        payload={
            "scope": 'enabled'
        }
    )
    for x in data:
        bots_ids.append(str(x["id"]))
    print(bots_ids)
    for bot in bots_ids:
        error, data = p3cw.request(
            entity="bots",
            action="panic_sell_all_deals",
            action_id=bot,
        )
    return bots_ids


################################

def start_command(update, context):
    user = update.message.chat["id"]
    if user != allowed:
        update.message.reply_text(sorry)
    else:
        update.message.reply_text(
            "Welcome to your 3C PANIC BOT ")


def sell_command(update, context):
    india = update.message.chat["id"]
    if india != allowed:
        update.message.reply_text(sorry)
    else:
        if len(get_close_deals()) > 0:
            get_close_deals()
            update.message.reply_text("BOSS , Your deals are closed successfully. ❤  ")
        else:
            update.message.reply_text("BOSS , There's no deals to close.💰")


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(telegram_api, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("Start", start_command, run_async=True))
    dp.add_handler(CommandHandler("sell", sell_command, run_async=True))
    dp.add_error_handler(error)
    updater.start_polling(1, timeout=10)


if __name__ == "__main__":
    print(Fore.BLUE + z)
    time.sleep(2)
    print("Bot started.")
    main()
