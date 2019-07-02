# -*- coding: utf-8
# Core
from .base_store import BaseStore

# Model
from ..models import Channel, ChannelUser


class ChannelStore(BaseStore):
    """
    Channel stores
    """

    async def create(self, owner_id, name, is_channel):
        channel = Channel(owner_id=owner_id, name=name, is_channel=is_channel)
        channel = await channel.create()

        return channel

    async def set_name(self, channel, name):
        channel.name = name
        self._update_query = channel.update(name=channel.name)

        return channel

    async def add_user(self, channel_id, user_id):
        channel_user = ChannelUser(channel_id=channel_id, user_id=user_id)
        channel_user = await channel_user.create()

        return channel_user

    async def remove_user(self, channel_user):
        await channel_user.delete()

        return True
