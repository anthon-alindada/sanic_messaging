# -*- coding: utf-8
# Core
from datetime import datetime, timedelta

# Messaging context
from ... import messaging_context

# Exception
from ...exceptions import InvalidInput, NotFound


async def test_filter_message_filter_author_id(message_data):
    # Filter author_id invalid
    filter_library = messaging_context.filter_message()
    errors = None

    try:
        await filter_library.run(author_id='asdf')
    except InvalidInput:
        errors = await filter_library.get_errors()

    assert errors['author_id'] == ['author_id is invalid'], \
        'Should validate author_id if not integer'

    # Filter messages by author_id
    filter_library = messaging_context.filter_message()
    messages = await filter_library.run(author_id='1')

    for message in messages:
        assert message.author_id == 1, 'Should filter message by author_id'


async def test_filter_message_filter_channel_id(message_data):
    # Filter channel_id invalid
    filter_library = messaging_context.filter_message()
    errors = None

    try:
        await filter_library.run(channel_id='asdf')
    except InvalidInput:
        errors = await filter_library.get_errors()

    assert errors['channel_id'] == ['channel_id is invalid'], \
        'Should validate channel_id if not integer'

    # Filter messages by channel_id
    filter_library = messaging_context.filter_message()
    messages = await filter_library.run(channel_id='1')

    for message in messages:
        assert message.channel_id == 1, 'Should filter message by channel_id'


async def test_filter_message_filter_timestamp(message_data):
    # Filter timestamp_start invalid
    filter_library = messaging_context.filter_message()
    errors = None

    try:
        await filter_library.run(timestamp_start='test')
    except InvalidInput:
        errors = await filter_library.get_errors()

    assert errors['timestamp_start'] == ['timestamp_start is invalid'], \
        'Should validate timestamp_start if not epoch value'

    # Filter timestamp_end invalid
    filter_library = messaging_context.filter_message()
    errors = None

    try:
        await filter_library.run(timestamp_end='test')
    except InvalidInput:
        errors = await filter_library.get_errors()

    assert errors['timestamp_end'] == ['timestamp_end is invalid'], \
        'Should validate timestamp_end if not epoch value'

    # Filter timestamp start and end
    start = datetime.now() - timedelta(days=2920)
    end = datetime.now() - timedelta(days=365)

    filter_library = messaging_context.filter_message()
    channels = await filter_library.run(
        timestamp_start=start.strftime('%s'),
        timestamp_end=end.strftime('%s'))

    for channel in channels:
        assert channel.timestamp < end and channel.timestamp > start, \
            'Should filter channel by start and end timestamp'


async def test_filter_message_filter_edited_timestamp(message_data):
    # Filter edited_timestamp_start invalid
    filter_library = messaging_context.filter_message()
    errors = None

    try:
        await filter_library.run(edited_timestamp_start='test')
    except InvalidInput:
        errors = await filter_library.get_errors()

    assert errors['edited_timestamp_start'] == \
        ['edited_timestamp_start is invalid'], \
        'Should validate edited_timestamp_start if not epoch value'

    # Filter timestamp_end invalid
    filter_library = messaging_context.filter_message()
    errors = None

    try:
        await filter_library.run(edited_timestamp_end='test')
    except InvalidInput:
        errors = await filter_library.get_errors()

    assert errors['edited_timestamp_end'] == \
        ['edited_timestamp_end is invalid'], \
        'Should validate edited_timestamp_end if not epoch value'

    # Filter timestamp start and end
    start = datetime.now() - timedelta(days=2920)
    end = datetime.now() - timedelta(days=365)

    filter_library = messaging_context.filter_message()
    channels = await filter_library.run(
        edited_timestamp_start=start.strftime('%s'),
        edited_timestamp_end=end.strftime('%s'))

    for channel in channels:
        assert channel.edited_timestamp < end and \
            channel.edited_timestamp > start, \
            'Should filter channel by start and end timestamp'


async def test_filter_message_filter_message_id(channel_data):
    # Filter message_id invalid
    filter_library = messaging_context.filter_message()
    errors = None

    try:
        await filter_library.run(message_id='asdf')
    except InvalidInput:
        errors = await filter_library.get_errors()

    assert errors['message_id'] == ['message_id is invalid'], \
        'Should validate message_id if not integer'

    # Find message by message_id
    # Not found
    filter_library = messaging_context.filter_message()
    message = None
    try:
        message = await filter_library.run(message_id='12345')
    except NotFound:
        pass
    assert message is None, \
        'Should throw not found if message id does not exist'

    # Find message by message_id
    filter_library = messaging_context.filter_message()
    message = await filter_library.run(message_id='1')

    assert message.id == 1, 'Should find message by id'
