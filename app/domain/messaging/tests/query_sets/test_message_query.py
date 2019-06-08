# -*- coding: utf-8
# Core
import random
from datetime import datetime, timedelta

# Models
from ...models import Message

# Messaging context
from ... import messaging_context


async def test_find_message_by_id(message_data):
    message = await messaging_context.message_query().find_by_id(
        id=28239).find()
    assert message is None, 'Should return None if id does not exist'

    message = await messaging_context.message_query().find_by_id(id=1).find()
    assert isinstance(message, Message), 'Should get message by id'


async def test_filter_message_by_author_id(message_data):
    messages = await messaging_context.message_query().filter_by_author_id(
        author_id=1).filter()

    for message in messages:
        assert message.author_id == 1, \
            'Should filter all messages by author id'


async def test_filter_message_by_channel_id(channel_data, message_data):
    channel = random.choice(channel_data)

    messages = await messaging_context.message_query().filter_by_channel_id(
        channel_id=channel.id).filter()

    for message in messages:
        assert message.channel_id == channel.id, \
            'Should filter all messages by channel id'


async def test_filter_message_by_timestamp(message_data):
    date = datetime.now() - timedelta(days=2920)

    # Filter timestamp start
    messages = await messaging_context.message_query().filter_by_timestamp(
        start=date).filter()

    for message in messages:
        assert message.timestamp > date, \
            'Should filter message by start timestamp'

    # Filter timestamp end
    messages = await messaging_context.message_query().filter_by_timestamp(
        end=date).filter()

    for message in messages:
        assert message.timestamp < date, \
            'Should filter message by end timestamp'

    # Filter timestamp start and end
    start = date
    end = datetime.now() - timedelta(days=365)

    messages = await messaging_context.message_query().filter_by_timestamp(
        start=start, end=end).filter()

    for message in messages:
        assert message.timestamp < end and \
            message.timestamp > start, \
            'Should filter message by start and end timestamp'


async def test_filter_message_by_edited_timestamp(message_data):
    date = datetime.now() - timedelta(days=2920)

    # Filter edited_timestamp start
    messages = await messaging_context.message_query(
        ).filter_by_edited_timestamp(start=date).filter()

    for message in messages:
        assert message.edited_timestamp > date, \
            'Should filter message by start edited timestamp'

    # Filter edited timestamp end
    messages = await messaging_context.message_query(
        ).filter_by_edited_timestamp(end=date).filter()

    for message in messages:
        assert message.edited_timestamp < date, \
            'Should filter message by end edited timestamp'

    # Filter edited timestamp start and end
    start = date
    end = datetime.now() - timedelta(days=365)

    messages = await messaging_context.message_query(
        ).filter_by_edited_timestamp(start=start, end=end).filter()

    for message in messages:
        assert message.edited_timestamp < end and \
            message.edited_timestamp > start, \
            'Should filter message by start and end edited timestamp'
