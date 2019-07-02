# -*- coding: utf-8
# Core
import pytest

# Models
from app.domain.messaging.models import Channel, ChannelUser

# Messaging context
from ... import messaging_context


@pytest.fixture
def channel_store():
    return messaging_context.channel_store()


async def test_create(channel_data, channel_store):
    channel = await channel_store.create(
        name='New channel',
        owner_id=1,
        is_channel=False)

    assert channel.id is not None, 'Should create channel'
    assert isinstance(channel, Channel), 'Should create channel'


async def test_set_name(channel_data, channel_store):
    channel = channel_data[0]
    channel = await channel_store.set_name(channel=channel, name='New name')
    await channel_store.save()

    assert channel.name == 'New name', 'Should set channel name'


async def test_add_user(channel_data, channel_store):
    channel = channel_data[2]

    # Add first user to channel
    await channel_store.add_user(
        channel_id=channel.id, user_id=1)

    # Get channel user data and check if existing
    channel_user = await ChannelUser.query.where(
        ChannelUser.channel_id == channel.id).where(
            ChannelUser.user_id == 1).gino.first()

    assert channel_user.channel_id == channel.id, \
        'Should add user to a channel'
    assert channel_user.user_id == 1, 'Should add user to a channel'


async def test_remove_user(channel_data, channel_store):
    # Get first channel user object in database
    channel_user = await ChannelUser.query.gino.first()

    # Delete data / Remove channel user
    await channel_store.remove_user(channel_user)

    # Get channel user data and check if existing
    channel_user = await ChannelUser.query.where(
        ChannelUser.channel_id == channel_user.channel_id).where(
            ChannelUser.user_id == channel_user.user_id).gino.first()

    assert channel_user is None, 'Should remove user to a channel'
