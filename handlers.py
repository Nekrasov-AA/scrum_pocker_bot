from telegram import CallbackQuery, Update

from session import chat_sessions_mapping, Session


def greet_user(update, context):
    print('Bot has been started')
    update.message.reply_text('Hi! For voting type /poll, Jira ticket and participants')


def display_help(update, context):
    update.message.reply_text('To vote, enter the command /poll, Jira ticket and participants')


def start_poll(update, context):
    '''
    обработчик нового голосования
    '''
    chat_id = update.message.chat_id
    chat_sessions_mapping[chat_id] = Session(update)


def next_poll(update, context):
    '''
    обработчик следующего голосвания
    '''
    chat_id = update.message.chat_id

    if chat_id not in chat_sessions_mapping:
        update.message.reply_text('Voting has not yet taken place.')
        return

    session = chat_sessions_mapping[chat_id]
    session.reset(update)

def vote_handler(update:Update, context) -> None:
    query: CallbackQuery = update.callback_query
    chat_id = query.message.chat_id
    session = chat_sessions_mapping[chat_id]
    session.process(query)