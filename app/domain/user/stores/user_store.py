# -*- coding: utf-8
# Core
from .base_store import BaseStore

# Model
from ..models import User


class UserStore(BaseStore):
    """
    User stores
    """

    async def create(self, email, first_name, last_name, password):
        user = User(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user = await user.create()

        return user

    async def set_password(self, user, password):
        user.set_password(password)
        self._update_query = user.update(password=user.password)

        return user

    async def activate(self, user):
        user.active = True
        self._update_query = user.update(active=user.active)

        return user
