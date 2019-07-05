# -*- coding: utf-8
# Core
from .base_query import BaseQuery

# Model
from ..models import ChannelUser


class ChannelUserQuery(BaseQuery):
    """
    Channel user query set
    """

    def __init__(self):
        self._model = ChannelUser
        self._query = self._model.query

    def find_by_id(self, channel_id, user_id):
        self._query = self._query.where(
            self._model.channel_id == channel_id).where(
                self._model.user_id == user_id)

        return self
