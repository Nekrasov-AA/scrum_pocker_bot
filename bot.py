import ast
import logging
import random
from typing import Iterable
from urllib.parse import urljoin

from telegram import InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from media_content import keyboard, icons, rotating_light
from settings import API_KEY, JIRA_LINK

# logging.basicConfig(filename='bot.log', level=logging.DEBUG)

sessions = {}

voters = {}

session_users = []

archive_users = []

global_users = []

rating_keyboard = InlineKeyboardMarkup(keyboard)


def main():
    mybot = Updater(API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("poll", talk_to_me))
    dp.add_handler(CommandHandler("next", talk_to_me))
    dp.add_handler(CommandHandler("help", display_help))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CallbackQueryHandler(button))

    logging.info('Bot has been started')
    mybot.start_polling()
    mybot.idle()


def greet_user(update, context):
    print('Bot has been started')
    update.message.reply_text('Hi! For voting type /poll, Jira ticket and participants')


def display_help(update, context):
    update.message.reply_text('To vote, enter the command /poll, Jira ticket and participants')


def talk_to_me(update, context):
    user_text = update.message.text
    keys = []

    if user_text.split(" ")[0] == "/poll":
        session_users.clear()
        voters.clear()
        ticket = user_text.split(" ")[1]
        users = user_text.split(" ")[2:]

        for i in users:
            global_users.append(i)

        if users in [['@task_alert_bot'], []]:
            update.message.reply_text('Insert the real user for voting')
        else:
            # voters = {}
            for user in users:
                voters[user[1:]] = None

            update.message.reply_text(f'{rotating_light} Rate ticket: ' + urljoin(JIRA_LINK, ticket),
                                      reply_markup=rating_keyboard)

            message_id = update.message.message_id
            chat_id = update.message.chat_id
            sessions[f'{message_id}_{chat_id}'] = voters

    elif user_text.split(" ")[0] != "/poll" and user_text.find(
            JIRA_LINK) == 0:  # Запуск следующего голосования в сессии отправкой номера задачи
        sessions.clear()
        session_users.clear()
        for user in global_users:
            voters[user[1:]] = None

        update.message.reply_text(f'{rotating_light} Rate ticket: ' + urljoin(JIRA_LINK, user_text),
                                  reply_markup=rating_keyboard)

        message_id = update.message.message_id
        chat_id = update.message.chat_id
        sessions[f'{message_id}_{chat_id}'] = voters

    for ind in keyboard:  # Iterate all the keyboard values and save them in a separate list 'keys' for response
        if isinstance(ind, Iterable):
            for i in ind:
                keys.append(str(i))
        else:
            keys.append(str(ind))


def button(update, context) -> None:
    query = update.callback_query

    query.answer()

    voted_user = (ast.literal_eval(str(query)))['from']['first_name']
    voter_username = (ast.literal_eval(str(query)))['from']['username']
    selected_value = (ast.literal_eval(str(query)))['data']

    try:
        ticket = query.message.reply_to_message.text.split(" ")[1]
    except IndexError:
        ticket = query.message.reply_to_message.text

    message_id = query.message.reply_to_message.message_id
    chat_id = query.message.chat_id

    voters = sessions[f'{message_id}_{chat_id}']
    voters[voter_username] = selected_value
    voters[voted_user] = selected_value

    voters_names = (dict(list(voters.items())[len(voters) // 2:]))

    who_votes = str(voters_names).replace("\'", "").replace("{", "").replace("}", "").replace(", ", "\n")

    voter = f'{voted_user}: {icons[random.randint(0, len(icons))]}'

    for val in session_users:
        if voted_user in val:
            session_users.remove(val)
        elif 'End voting' in val:
            session_users.append(voter)
    else:
        session_users.append(voter)

    voted_users_final_list = ('\n'.join(session_users))

    if ticket.find(JIRA_LINK):
        pass
    else:
        ticket = urljoin(JIRA_LINK, ticket)

    query.edit_message_text(
        text=f'{voted_users_final_list} \n {rotating_light} Rate ticket: ' + ticket,
        reply_markup=rating_keyboard)

    if all(voters.values()):
        query.edit_message_text(
            text=f'Voting ended:\n{who_votes} \n {rotating_light} Rated ticket: ' + urljoin(JIRA_LINK, ticket),
            reply_markup=rating_keyboard)

        archive_users.append(who_votes)

    if selected_value == 'End voting':
        try:
            users = archive_users[len(archive_users) - 2]
            query.edit_message_text(
                text=f'Voting ended:\n{users}\n {rotating_light} Rated ticket: ' + urljoin(JIRA_LINK, ticket))
        except IndexError:
            query.edit_message_text(
                text=f'Voting ended manually\n {rotating_light} Rated ticket: ' + urljoin(
                    JIRA_LINK, ticket))


if __name__ == "__main__":
    main()
