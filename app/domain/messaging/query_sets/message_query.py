# -*- coding: utf-8
# Core
from .base_query import BaseQuery

# Model
from ..models import Message


class MessageQuery(BaseQuery):
    """
    Message query set
    """

    def __init__(self):
        self._model = Message
        self._query = self._model.query

    def find_by_id(self, id):
        self._query = self._query.where(self._model.id == id)
        return self

    def filter_by_author_id(self, author_id):
        self._query = self._query.where(self._model.author_id == author_id)
        return self

    def filter_by_channel_id(self, channel_id):
        self._query = self._query.where(self._model.channel_id == channel_id)
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
