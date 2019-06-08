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


async def test_create_message_invalid_form(message_data, create_message_lib):
    errors = None
    try:
        await create_message_lib.run(content='', author_id=1, channel_id=1)
    except InvalidInput:
        errors = await create_message_lib.get_errors()

    assert errors is not None, 'Should fail if form has an error'


async def test_create_message(message_data, create_message_lib):
    message = await create_message_lib.run(
        content='New message', author_id=1, channel_id=1)

    assert isinstance(message, Message), 'Should create message'
