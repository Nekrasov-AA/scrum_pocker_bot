import logging
from enum import Enum
from random import choice
from typing import Dict, List, Optional
from urllib.parse import urljoin

from telegram import CallbackQuery, Message, Update

from media_content import rotating_light, rating_keyboard, icons
from settings import JIRA_LINK

chat_sessions_mapping: Dict[str, 'Session'] = {}  # маппинг чат -- сессия голосвания в чате

class SessionStatus(Enum):
    ongoing = 1
    finished = 2

class Session:
    def __init__(self, update: Update):
        self.update = update
        init_message = update.message.text

        # достаем из сообщения список пользователей и тему
        self.ticket = init_message.split(" ")[1]

        # удаляем у имени пользователя первый символ -- @
        self.users = [user[1:] for user in init_message.split(" ")[2:]]

        # если список пользователей невалидный -- говорим об этом
        if not self.is_valid_users(self.users):
            update.message.reply_text('not valid users')

        self.status = SessionStatus.ongoing

        # начинаем голосование
        self.start_voting()

    def start_voting(self):
        # инициализируем список голосов пользователй
        self.user_votes = {user: None for user in self.users}
        self.send_voting_message()

    def reset(self, new_update):
        self.status = SessionStatus.ongoing
        self.update = new_update
        self.ticket = new_update.message.text
        self.start_voting()

    def set_user_data(self, user, vote: CallbackQuery):
        self.user_votes[user] = vote

    def process(self, query: CallbackQuery):
        # TODO расхардкодить
        if query.data == 'End voting':
            self.status = SessionStatus.finished
            self.send_finish_voting_message()
            return

        logging.debug(f'set user data {query.from_user.username, query.data, query.id}')
        self.set_user_data(query.from_user.username, query)

        if all(vote is not None for vote in self.user_votes.values()):
            self.status = SessionStatus.finished
            self.send_finish_voting_message()
        else:
            self.update_voting_message()

    def get_vote_value(self, vote:Optional[CallbackQuery]) -> str:
        if not vote or self.status is SessionStatus.ongoing:
            return choice(icons)
        else:
            return vote.data


    def get_poll_list_message(self) -> str:
        return '\n'.join([f'{user}: {self.get_vote_value(vote)}' for user, vote in self.user_votes.items()])

    def send_finish_voting_message(self):
        self.voting_message.edit_text(text=f'Voting ended for {self.ticket}\n{self.get_poll_list_message()}')

    def send_voting_message(self):
        self.voting_message = self.update.message.reply_text(
            f'{rotating_light} Rate ticket: {urljoin(JIRA_LINK, self.ticket)}\n{self.get_poll_list_message()}',
            reply_markup=rating_keyboard
        )

    def update_voting_message(self):
        self.voting_message.edit_text(
            f'{rotating_light} Rate ticket: {urljoin(JIRA_LINK, self.ticket)}\n{self.get_poll_list_message()}',
            reply_markup=rating_keyboard
        )

    def is_valid_users(self, users: List[str]):
        '''
        TODO описать как валидируем
        :param users:
        :return:
        '''
        if len(users) == 0:
            return False

        if '@task_alert_bot' in users:
            return False

        return True
