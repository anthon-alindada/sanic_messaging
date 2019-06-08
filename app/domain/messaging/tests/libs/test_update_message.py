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


async def test_update_message_invalid_form(message_data, update_message_lib):
    errors = None
    try:
        await update_message_lib.run(
            content='', author_id=1, message_instance=message_data[0])
    except InvalidInput:
        errors = await update_message_lib.get_errors()

    assert errors is not None, 'Should fail if form has an error'


async def test_update_message(message_data, update_message_lib):
    message = await update_message_lib.run(
        content='Updated message content',
        author_id=message_data[0].author_id,
        message_instance=message_data[0])

    assert isinstance(message, Message), 'Should update message'
    assert message.content == 'Updated message content', \
        'Should update message'
