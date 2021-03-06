# -*- coding: utf-8
# Core
from .base_query import BaseQuery

# Model
from ..models import Channel, ChannelUser


class ChannelQuery(BaseQuery):
    """
    Channel query set
    """

    def __init__(self):
        self._model = Channel
        self._query = self._model.query
        self._channel_user_model = ChannelUser

    def find_by_id(self, id):
        self._query = self._query.where(self._model.id == id)
        return self

    def filter_by_owner_id(self, owner_id):
        self._query = self._query.where(self._model.owner_id == owner_id)
        return self

    def filter_by_is_channel(self, is_channel):
        self._query = self._query.where(self._model.is_channel.is_(is_channel))
        return self

    def filter_by_timestamp(self, start=None, end=None):
        if start:
            self._query = self._query.where(self._model.timestamp > start)

        if end:
            self._query = self._query.where(self._model.timestamp < end)

        return self

    def filter_by_edited_timestamp(self, start=None, end=None):
        if start:
            self._query = self._query.where(
                self._model.edited_timestamp > start)

        if end:
            self._query = self._query.where(
                self._model.edited_timestamp < end)

        return self

    def filter_by_user_id(self, user_id):
        self._query = self._query.select_from(
            self._model.join(self._channel_user_model)).where(
                self._channel_user_model.user_id == user_id)

        return self
