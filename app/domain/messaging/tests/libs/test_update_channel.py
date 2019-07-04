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


async def test_update_channel_blank_name(channel_data, update_channel_lib):
    errors = None

    # Test name is blank
    try:
        await update_channel_lib.run(
            name='', owner_id=1, channel_instance=channel_data[0])
    except InvalidInput:
        errors = await update_channel_lib.get_errors()

    assert errors.get('name') == ['Name is required'], \
        'Should fail if name is blank'


async def test_update_channel_long_name(channel_data, update_channel_lib):
    errors = None

    # Test name is more than 50 characters
    try:
        await update_channel_lib.run(
            name='aasdfghjklsasdfghjklsasdfghjklsasdfghjklsasdfghjssdfghjkls',
            owner_id=1,
            channel_instance=channel_data[0])
    except InvalidInput:
        errors = await update_channel_lib.get_errors()

    assert errors.get(
        'name') == ['Name must be less than or equal to 50 characters'], \
        'Should fail if name is more than 50 characters'


async def test_update_channel_not_channel(channel_data, update_channel_lib):
    errors = None

    # Get channel instance
    channel_instance = None
    for channel in channel_data:
        if channel.is_channel is False:
            channel_instance = channel
            break

    # Test cannot update if is_channel is False
    try:
        await update_channel_lib.run(
            name='updated name',
            owner_id=1,
            channel_instance=channel_instance)
    except InvalidInput:
        errors = await update_channel_lib.get_errors()

    assert errors.get('name') == ['Cannot update channel'], \
        'Should fail if channel instance is not a channel'


async def test_update_channel_not_owner(channel_data, update_channel_lib):
    errors = None

    # Test if not same owner_id
    try:
        await update_channel_lib.run(
            name='Update', owner_id=2, channel_instance=channel_data[0])
    except InvalidInput:
        errors = await update_channel_lib.get_errors()

    assert errors.get('name') == ['Unauthorized to update channel'], \
        'Should fail if not owner'


async def test_update_channel(channel_data, update_channel_lib):
    channel = await update_channel_lib.run(
        name='Updated Channel Name',
        owner_id=channel_data[0].owner_id,
        channel_instance=channel_data[0])

    assert isinstance(channel, Channel), 'Should update channel'
    assert channel.name == 'Updated Channel Name', 'Should update channel'
