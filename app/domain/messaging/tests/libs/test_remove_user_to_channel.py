# -*- coding: utf-8
# Core
import pytest

# Exception
from ...exceptions import InvalidInput

# Messaging context
from ... import messaging_context


@pytest.fixture
def remove_user_to_channel_lib():
    return messaging_context.remove_user_to_channel()


@pytest.fixture
def add_user_to_channel_lib():
    return messaging_context.add_user_to_channel()


async def test_remove_user_to_channel_user_id_required(
    channel_data,
    remove_user_to_channel_lib
):
    errors = None
    try:
        await remove_user_to_channel_lib.run(
            channel_instance=channel_data[3], user_id=None)
    except InvalidInput:
        errors = await remove_user_to_channel_lib.get_errors()

    assert errors['user_id'] == ['user_id is required'], \
        'Should fail if no user id'


async def test_remove_user_to_channel_user_id_invalid(
    channel_data,
    remove_user_to_channel_lib
):
    errors = None
    try:
        await remove_user_to_channel_lib.run(
            channel_instance=channel_data[3], user_id='asdf')
    except InvalidInput:
        errors = await remove_user_to_channel_lib.get_errors()

    assert errors['user_id'] == ['user_id is invalid'], \
        'Should fail if user_id is invalid or not integer'


async def test_remove_user_to_channel_user_id_not_found(
    channel_data,
    remove_user_to_channel_lib
):
    errors = None
    try:
        await remove_user_to_channel_lib.run(
            channel_instance=channel_data[3], user_id=1239123891)
    except InvalidInput:
        errors = await remove_user_to_channel_lib.get_errors()

    assert errors['user_id'] == ['user does not exist'], \
        'Should fail if user_id is not added to channel'


async def test_remove_user_to_channel(
    channel_data,
    remove_user_to_channel_lib,
    add_user_to_channel_lib,
):
    await remove_user_to_channel_lib.run(
        channel_instance=channel_data[0], user_id=1)

    # After removal testing is successful add it again for other testing
    await add_user_to_channel_lib.run(
        channel_instance=channel_data[0], user_id=1)
