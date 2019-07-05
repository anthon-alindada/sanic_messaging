# -*- coding: utf-8
# Core
import pytest

# Models
from app.domain.messaging.models import Message

# Exception
from app.domain.messaging.exceptions import InvalidInput

# Messaging context
from ... import messaging_context


@pytest.fixture
def create_message_lib():
    return messaging_context.create_message()


async def test_create_message_blank_content(message_data, create_message_lib):
    errors = {}

    try:
        await create_message_lib.run(content='', author_id=1, channel_id=1)
    except InvalidInput:
        errors = await create_message_lib.get_errors()

    assert errors.get('content') == ['Content is required'], \
        'Should fail if content is blank'


async def test_create_message_long_content(message_data, create_message_lib):
    errors = {}

    try:
        await create_message_lib.run(
            content='aaasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjsdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjsdfjksadlfj',  # noqa
            author_id=1,
            channel_id=1)
    except InvalidInput:
        errors = await create_message_lib.get_errors()

    assert errors.get(
        'content') == ['Content must be less than or equal to 255 characters'], 'Should fail if content is too long'  # noqa


async def test_create_message_valid_content(message_data, create_message_lib):
    errors = {}

    await create_message_lib.run(
        content='Valid content', author_id=1, channel_id=1)

    assert errors.get('content') is None, 'Should fail if content is valid'


async def test_create_message(message_data, create_message_lib):
    message = await create_message_lib.run(
        content='New message', author_id=1, channel_id=1)

    assert isinstance(message, Message), 'Should create message'
