import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from commands import commands
from handlers import vote_handler, next_poll

with open('API_KEY', 'r') as f:
    API_KEY = f.read()

logging.basicConfig(level=logging.DEBUG)


# TODO глобальные переменные должны иметь норм имена
# sessions = {}

voters = {}

session_users = []

archive_users = []

global_users = []


def main():
    mybot = Updater(API_KEY, use_context=True)

    dp = mybot.dispatcher

    # TODO сделать отдельный словарь с коммандами и добавлять в диспетчер оттуда
    for command, handler in commands.items():
        dp.add_handler(CommandHandler(command, handler))

    dp.add_handler(MessageHandler(Filters.text, next_poll))
    dp.add_handler(CallbackQueryHandler(vote_handler))

    logging.info('Bot has been started')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
