from telegram import CallbackQuery, Update
from telegram.ext import ContextTypes

from session import chat_sessions_mapping, Session


async def greet_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('Bot has been started')
    await update.message.reply_text('Hi! For voting type /poll, Jira ticket and participants')


async def display_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('To vote, enter the command /poll, Jira ticket and participants')


async def start_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for new voting session
    """
    chat_id = update.message.chat_id
    chat_sessions_mapping[chat_id] = await Session.create(update)


async def next_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for next voting session
    """
    chat_id = update.message.chat_id

    if chat_id not in chat_sessions_mapping:
        await update.message.reply_text('Voting has not yet taken place.')
        return

    session = chat_sessions_mapping[chat_id]
    await session.reset(update)

async def vote_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query: CallbackQuery = update.callback_query
    chat_id = query.message.chat_id
    session = chat_sessions_mapping[chat_id]
    await session.process(query)