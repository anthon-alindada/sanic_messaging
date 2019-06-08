# -*- coding: utf-8
# Core
import pytest

# Models
from app.domain.messaging.models import Channel

# Exception
from app.domain.messaging.exceptions import InvalidInput

# Messaging context
from ... import messaging_context


@pytest.fixture
def create_channel_lib():
    return messaging_context.create_channel()


async def test_create_channel_invalid_form(channel_data, create_channel_lib):
    errors = None
    try:
        await create_channel_lib.run(name='', owner_id=1, is_channel=True)
    except InvalidInput:
        errors = await create_channel_lib.get_errors()

    assert errors is not None, 'Should fail if form has an error'


async def test_create_channel(channel_data, create_channel_lib):
    channel = await create_channel_lib.run(
        name='New Channel', owner_id=1, is_channel=True)

    assert isinstance(channel, Channel), 'Should create channel'
    assert channel.is_channel is True, 'Should create channel'

    channel = await create_channel_lib.run(
        name='New Private Channel', owner_id=1, is_channel=False)

    assert isinstance(channel, Channel), 'Should create private channel'
    assert channel.name == 'New Private Channel', \
        'Should create private channel'
    assert channel.is_channel is False, 'Should create private channel'
