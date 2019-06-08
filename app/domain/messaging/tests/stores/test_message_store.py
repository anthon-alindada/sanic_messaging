# -*- coding: utf-8
# Core
import pytest

# Models
from app.domain.messaging.models import Message

# Messaging context
from ... import messaging_context


@pytest.fixture
def message_store():
    return messaging_context.message_store()


async def test_create(message_data, message_store):
    message = await message_store.create(
        content='This is a sample message',
        author_id=1,
        channel_id=1)

    assert message.id is not None, 'Should create message'
    assert isinstance(message, Message), 'Should create message'


async def test_set_content(message_data, message_store):
    message = message_data[0]
    message = await message_store.set_content(
        message=message, content='New content')
    await message_store.save()

    assert message.content == 'New content', 'Should set message content'
