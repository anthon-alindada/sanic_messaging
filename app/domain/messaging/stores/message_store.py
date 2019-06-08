# -*- coding: utf-8
# Core
from .base_store import BaseStore

# Model
from ..models import Message


class MessageStore(BaseStore):
    """
    Message stores
    """

    async def create(self, content, author_id, channel_id):
        message = Message(
            content=content, author_id=author_id, channel_id=channel_id)
        message = await message.create()

        return message

    async def set_content(self, message, content):
        message.content = content
        self._update_query = message.update(content=message.content)

        return message
