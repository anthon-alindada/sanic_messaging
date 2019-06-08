# -*- coding: utf-8
# Core
import pytest

# Models
from app.domain.messaging.models import Channel

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
