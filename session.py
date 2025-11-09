import logging
from enum import Enum
from random import choice
from typing import Dict, List, Optional
from urllib.parse import urljoin

from telegram import CallbackQuery, Message, Update

from media_content import rotating_light, rating_keyboard, icons
from settings import JIRA_LINK

chat_sessions_mapping: Dict[str, 'Session'] = {}  # mapping: chat -> voting session in chat


class SessionStatus(Enum):
    ongoing = 1
    finished = 2
    closed = 3


class Session:
    def __init__(self, update: Update):
        self.update = update
        init_message = update.message.text

        # extract list of users and topic from message
        self.ticket = init_message.split(" ")[1]

        # remove first character (@) from username
        self.users = [user[1:] for user in init_message.split(" ")[2:]]

        self.status = SessionStatus.ongoing
    
    @classmethod
    async def create(cls, update: Update):
        """Async constructor for Session"""
        session = cls(update)
        
        # if user list is invalid - inform about it
        if not session.is_valid_users(session.users):
            await update.message.reply_text('not valid users')
            return session

        # start voting
        await session.start_voting()
        return session

    async def start_voting(self):
        # initialize user votes list
        self.user_votes = {user: None for user in self.users}
        self.user_votes_placeholders = {}
        await self.send_voting_message()

    async def reset(self, new_update):
        await self.close_voting()
        self.status = SessionStatus.ongoing
        self.update = new_update
        self.ticket = new_update.message.text
        await self.start_voting()

    def set_user_data(self, user, vote: CallbackQuery):
        self.user_votes[user] = vote

    async def close_voting(self):
        self.status = SessionStatus.closed
        await self.send_finish_voting_message()

    async def process(self, query: CallbackQuery):
        # TODO remove hardcode
        if query.data == 'End voting':
            await self.close_voting()
            return

        logging.debug(f'set user data {query.from_user.username, query.data, query.id}')
        self.set_user_data(query.from_user.username, query)

        if all(vote is not None for vote in self.user_votes.values()):
            self.status = SessionStatus.finished
            await self.send_finish_voting_message()
        else:
            await self.update_voting_message()

    def get_vote_value(self, vote: Optional[CallbackQuery]) -> str:
        if self.status is SessionStatus.ongoing:
            if vote:
                placeholder = self.user_votes_placeholders.get(vote.from_user.username, choice(icons))
                self.user_votes_placeholders[vote.from_user.username] = placeholder
                return placeholder
            else:
                return '-'
        else:
            return vote.data if vote else '-'

    def get_poll_list_message(self) -> str:
        return '\n'.join(
            # TODO replace user username with firstname
            # need to consider that until user votes we don't know their data, maybe need to register users somehow
            [f'{user}: {self.get_vote_value(vote)}'
             for user, vote in self.user_votes.items()]
        )

    async def send_finish_voting_message(self):
        await self.voting_message.edit_text(
            text=f'Voting ended for {self.ticket}\n{self.get_poll_list_message()}',
            reply_markup=rating_keyboard if self.status is SessionStatus.finished else None
        )

    async def send_voting_message(self):
        self.voting_message = await self.update.message.reply_text(
            f'{rotating_light} Rate ticket: {urljoin(JIRA_LINK, self.ticket)}\n{self.get_poll_list_message()}',
            reply_markup=rating_keyboard
        )

    async def update_voting_message(self):
        await self.voting_message.edit_text(
            f'{rotating_light} Rate ticket: {urljoin(JIRA_LINK, self.ticket)}\n{self.get_poll_list_message()}',
            reply_markup=rating_keyboard
        )

    def is_valid_users(self, users: List[str]):
        """
        TODO describe how we validate users
        :param users: list of usernames
        :return: True if users are valid
        """
        if len(users) == 0:
            return False

        if '@task_alert_bot' in users:
            return False

        return True
