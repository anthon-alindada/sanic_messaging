# -*- coding: utf-8
# Core
from .base_store import BaseStore

# Model
from ..models import Channel


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
