# -*- coding: utf-8
# Models
from ..models import Channel, ChannelUser, Message


async def test_channel_model(channel_data):
    channel = Channel(
        owner_id=1,
        name='General')

    channel = await channel.create()

    assert repr(channel) == "<Channel: 'General'>"


async def test_channel_user_model(channel_data):
    channel_user = ChannelUser(
        user_id=1,
        channel_id=1)

    channel_user = await channel_user.create()

    assert repr(channel_user) == "<ChannelUser: 1 1>"


async def test_message_model(message_data):
    message = Message(
        author_id=1,
        channel_id=1,
        content='General')

    message = await message.create()

    assert repr(message) == "<Message: {}>".format(message.id)
