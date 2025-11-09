import logging

from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext import filters

from commands import commands
from handlers import vote_handler, next_poll

with open('API_KEY', 'r') as f:
    API_KEY = f.read().strip()

logging.basicConfig(level=logging.DEBUG)


# TODO global variables should have proper names
# sessions = {}

voters = {}

session_users = []

archive_users = []

global_users = []


async def main():
    # Create the Application
    app = Application.builder().token(API_KEY).build()

    # TODO create separate dictionary for commands and add them to dispatcher from there
    for command, handler in commands.items():
        app.add_handler(CommandHandler(command, handler))

    app.add_handler(MessageHandler(filters.TEXT, next_poll))
    app.add_handler(CallbackQueryHandler(vote_handler))

    logging.info('Bot has been started')
    
    # Start the bot
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
