# -*- coding: utf-8
# Core
import pytest

# Exception
from ...exceptions import InvalidInput

# Models
from app.domain.messaging.models import ChannelUser

# Messaging context
from ... import messaging_context


@pytest.fixture
def add_user_to_channel_lib():
    return messaging_context.add_user_to_channel()


async def test_add_user_to_channel_user_id_required(
    channel_data,
    add_user_to_channel_lib
):
    errors = None
    try:
        await add_user_to_channel_lib.run(
            channel_instance=channel_data[3], user_id=None)
    except InvalidInput:
        errors = await add_user_to_channel_lib.get_errors()

    assert errors is not None, 'Should fail if no user id'
    assert errors['user_id'] == 'user_id is required', \
        'Should fail if no user id'


async def test_add_user_to_channel_invalid_user_id(
    channel_data,
    add_user_to_channel_lib
):
    errors = None
    try:
        await add_user_to_channel_lib.run(
            channel_instance=channel_data[3], user_id='asdfasdf')
    except InvalidInput:
        errors = await add_user_to_channel_lib.get_errors()

    assert errors is not None, 'Should fail if user id is invalid'
    assert errors['user_id'] == 'user_id is invalid', \
        'Should fail if user id is invalid'


async def test_add_user_to_channel_already_added_to_channel(
    channel_data,
    add_user_to_channel_lib
):
    errors = None
    try:
        await add_user_to_channel_lib.run(
            channel_instance=channel_data[0], user_id=1)
    except InvalidInput:
        errors = await add_user_to_channel_lib.get_errors()

    assert errors is not None, 'Should fail if user already added to channel'
    assert errors['user_id'] == 'user_id already added', \
        'Should fail if user id is invalid'


async def test_add_user_to_channel(
    channel_data,
    add_user_to_channel_lib
):
    channel_user = await add_user_to_channel_lib.run(
        channel_instance=channel_data[1], user_id=1)

    assert isinstance(channel_user, ChannelUser), 'Should add user to channel'
