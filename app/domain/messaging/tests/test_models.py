# -*- coding: utf-8
# Models
from ..models import Channel, Message


async def test_channel_model(channel_data):
    channel = Channel(
        owner_id=1,
        name='General')

    channel = await channel.create()

    assert repr(channel) == "<Channel: 'General'>"


async def test_message_model(message_data):
    message = Message(
        author_id=1,
        channel_id=1,
        content='General')

    message = await message.create()

    assert repr(message) == "<Message: {}>".format(message.id)
