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


async def test_create_channel_blank_name(channel_data, create_channel_lib):
    errors = {}

    # Test name is blank
    try:
        create_channel_lib = messaging_context.create_channel()
        await create_channel_lib.run(name='', owner_id=1, is_channel=True)
    except InvalidInput:
        errors = await create_channel_lib.get_errors()

    assert errors.get('name') == ['Name is required'], \
        'Should fail if form has an error'


async def test_create_channel_long_name(channel_data, create_channel_lib):
    errors = {}

    # Test name is more than 50 characters
    try:
        create_channel_lib = messaging_context.create_channel()
        await create_channel_lib.run(
            name='aasdfghjklsasdfghjklsasdfghjklsasdfghjklsasdfghjssdfghjkls',
            owner_id=1,
            is_channel=True)
    except InvalidInput:
        errors = await create_channel_lib.get_errors()

    assert errors.get(
        'name') == ['Name must be less than or equal to 50 characters'], \
        'Should fail if form has an error'


async def test_create_channel_valid_name(channel_data, create_channel_lib):
    errors = {}

    # Test name is valid
    create_channel_lib = messaging_context.create_channel()
    await create_channel_lib.run(
        name='Name',
        owner_id=1,
        is_channel=True)

    assert errors.get('name') is None, 'Should fail if form has an error'


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
