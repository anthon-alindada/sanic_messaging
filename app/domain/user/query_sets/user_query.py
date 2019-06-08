# -*- coding: utf-8
# Core
from .base_query import BaseQuery

# Model
from ..models import User


class UserQuery(BaseQuery):
    """
    User query set
    """

    def __init__(self):
        self._model = User
        self._query = self._model.query

    def find_by_id(self, id):
        self._query = self._query.where(self._model.id == id)
        return self

    def find_by_email(self, email):
        self._query = self._query.where(self._model.email == email)
        return self

    def filter_by_active(self):
        self._query = self._query.where(self._model.active.is_(True))
        return self

    def filter_by_inactive(self):
        self._query = self._query.where(self._model.active.is_(False))
        return self
