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
def update_channel_lib():
    return messaging_context.update_channel()


async def test_update_channel_invalid_form(channel_data, update_channel_lib):
    errors = None
    try:
        await update_channel_lib.run(
            name='', owner_id=1, channel_instance=channel_data[0])
    except InvalidInput:
        errors = await update_channel_lib.get_errors()

    assert errors is not None, 'Should fail if form has an error'


async def test_update_channel(channel_data, update_channel_lib):
    channel = await update_channel_lib.run(
        name='Updated Channel Name',
        owner_id=channel_data[0].owner_id,
        channel_instance=channel_data[0])

    assert isinstance(channel, Channel), 'Should update channel'
    assert channel.name == 'Updated Channel Name', 'Should update channel'
