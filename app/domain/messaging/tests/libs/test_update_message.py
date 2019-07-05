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
def update_message_lib():
    return messaging_context.update_message()


async def test_update_message_blank_content(message_data, update_message_lib):
    errors = {}

    try:
        await update_message_lib.run(
            content='', author_id=1, message_instance=message_data[0])
    except InvalidInput:
        errors = await update_message_lib.get_errors()

    assert errors.get('content') == ['Content is required'], \
        'Should fail if content is blank'


async def test_update_message_long_content(message_data, update_message_lib):
    errors = {}

    try:
        await update_message_lib.run(
            content='aaasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjsdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjasdfjksadlfjsdfjksadlfj',  # noqa
            author_id=1,
            message_instance=message_data[0])
    except InvalidInput:
        errors = await update_message_lib.get_errors()

    assert errors.get(
        'content') == ['Content must be less than or equal to 255 characters'], 'Should fail if content is too long'  # noqa


async def test_update_message_different_author_content(
    message_data,
    update_message_lib
):
    errors = {}

    try:
        await update_message_lib.run(
            content='Content', author_id=2, message_instance=message_data[0])
    except InvalidInput:
        errors = await update_message_lib.get_errors()

    assert errors.get('content') == ['Unauthorized to update message'], \
        'Should fail if not the same author'


async def test_update_message_valid_content(message_data, update_message_lib):
    errors = {}

    await update_message_lib.run(
        content='Content',  # noqa
        author_id=1,
        message_instance=message_data[0])

    assert errors.get('content') is None, 'Should fail if content is valid'


async def test_update_message(message_data, update_message_lib):
    message = await update_message_lib.run(
        content='Updated message content',
        author_id=message_data[0].author_id,
        message_instance=message_data[0])

    assert isinstance(message, Message), 'Should update message'
    assert message.content == 'Updated message content', \
        'Should update message'
