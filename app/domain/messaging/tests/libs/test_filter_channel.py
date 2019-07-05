# -*- coding: utf-8
# Core
from datetime import datetime, timedelta

# Messaging context
from ... import messaging_context

# Exception
from ...exceptions import InvalidInput, NotFound

# Model
from ...models import ChannelUser


async def test_filter_channel_filter_owner_id(channel_data):
    # Filter owner_id invalid
    filter_library = messaging_context.filter_channel()
    errors = None

    try:
        await filter_library.run(owner_id='asdf')
    except InvalidInput:
        errors = await filter_library.get_errors()

    assert errors['owner_id'] == ['owner_id is invalid'], \
        'Should validate owner_id if not integer'

    # Filter channels by owner_id
    filter_library = messaging_context.filter_channel()
    channels = await filter_library.run(owner_id='1')

    for channel in channels:
        assert channel.owner_id == 1, 'Should filter channel by owner id'


async def test_filter_channel_filter_is_channel(channel_data):
    # Filter is_channel invalid
    filter_library = messaging_context.filter_channel()
    errors = None

    try:
        await filter_library.run(is_channel='abc')
    except InvalidInput:
        errors = await filter_library.get_errors()

    assert errors['is_channel'] == ['is_channel is invalid'], \
        'Should validate is_channel if not true or false string'

    # Filter channels by is_channel
    filter_library = messaging_context.filter_channel()
    channels = await filter_library.run(is_channel='true')

    for channel in channels:
        assert channel.is_channel is True, \
            'Should filter channel by is_channel'

    filter_library = messaging_context.filter_channel()
    channels = await filter_library.run(is_channel='False')

    for channel in channels:
        assert channel.is_channel is False, \
            'Should filter channel by is_channel'


async def test_filter_channel_filter_timestamp(channel_data):
    # Filter timestamp_start invalid
    filter_library = messaging_context.filter_channel()
    errors = None

    try:
        await filter_library.run(timestamp_start='test')
    except InvalidInput:
        errors = await filter_library.get_errors()

    assert errors['timestamp_start'] == ['timestamp_start is invalid'], \
        'Should validate timestamp_start if not epoch value'

    # Filter timestamp_end invalid
    filter_library = messaging_context.filter_channel()
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

    filter_library = messaging_context.filter_channel()
    channels = await filter_library.run(
        timestamp_start=start.strftime('%s'),
        timestamp_end=end.strftime('%s'))

    for channel in channels:
        assert channel.timestamp < end and channel.timestamp > start, \
            'Should filter channel by start and end timestamp'


async def test_filter_channel_filter_edited_timestamp(channel_data):
    # Filter edited_timestamp_start invalid
    filter_library = messaging_context.filter_channel()
    errors = None

    try:
        await filter_library.run(edited_timestamp_start='test')
    except InvalidInput:
        errors = await filter_library.get_errors()

    assert errors['edited_timestamp_start'] == \
        ['edited_timestamp_start is invalid'], \
        'Should validate edited_timestamp_start if not epoch value'

    # Filter timestamp_end invalid
    filter_library = messaging_context.filter_channel()
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

    filter_library = messaging_context.filter_channel()
    channels = await filter_library.run(
        edited_timestamp_start=start.strftime('%s'),
        edited_timestamp_end=end.strftime('%s'))

    for channel in channels:
        assert channel.edited_timestamp < end and \
            channel.edited_timestamp > start, \
            'Should filter channel by start and end timestamp'


async def test_filter_channel_filter_channel_id(channel_data):
    # Filter channel_id invalid
    filter_library = messaging_context.filter_channel()
    errors = None

    try:
        await filter_library.run(channel_id='asdf')
    except InvalidInput:
        errors = await filter_library.get_errors()

    assert errors['channel_id'] == ['channel_id is invalid'], \
        'Should validate channel_id if not integer'

    # Filter channels by owner_id
    # Not found
    filter_library = messaging_context.filter_channel()
    channel = None
    try:
        channel = await filter_library.run(channel_id='12341')
    except NotFound:
        pass
    assert channel is None, \
        'Should throw not found if channel id does not exist'

    # Filter channels by owner_id
    filter_library = messaging_context.filter_channel()
    channel = await filter_library.run(channel_id='1')

    assert channel.id == 1, 'Should find channel by id'


async def test_filter_channel_filter_by_user_id(channel_data):
    # Filter owner_id invalid
    filter_library = messaging_context.filter_channel()
    errors = None

    try:
        await filter_library.run(user_id='asdf')
    except InvalidInput:
        errors = await filter_library.get_errors()

    assert errors['user_id'] == ['user_id is invalid'], \
        'Should validate user_id if not integer'

    # Filter channels by user_id
    filter_library = messaging_context.filter_channel()
    channels = await filter_library.run(user_id='1')

    for channel in channels:
        # Check if channel user existing
        channel_user = await ChannelUser.query.where(
            ChannelUser.channel_id == channel.id).where(
                ChannelUser.user_id == 1).gino.first()

        assert channel_user is not None, \
            'Should filter all channels by user id'
