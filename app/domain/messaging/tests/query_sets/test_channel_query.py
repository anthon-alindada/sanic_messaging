# -*- coding: utf-8
# Core
from datetime import datetime, timedelta

# Models
from ...models import Channel

# Messaging context
from ... import messaging_context


async def test_find_channel_by_id(channel_data):
    channel = await messaging_context.channel_query().find_by_id(
        id=28239).find()
    assert channel is None, 'Should return None if id does not exist'

    channel = await messaging_context.channel_query().find_by_id(id=1).find()
    assert isinstance(channel, Channel), 'Should get channel by id'


async def test_filter_channel_by_owner_id(channel_data):
    channels = await messaging_context.channel_query().filter_by_owner_id(
        owner_id=1).filter()

    for channel in channels:
        assert channel.owner_id == 1, 'Should filter all channels by owner id'


async def test_filter_channel_by_is_channel(channel_data):
    channels = await messaging_context.channel_query().filter_by_is_channel(
        is_channel=True).filter()

    for channel in channels:
        assert channel.is_channel is True, \
            'Should filter all channels by is_channel true'

    channels = await messaging_context.channel_query().filter_by_is_channel(
        is_channel=False).filter()

    for channel in channels:
        assert channel.is_channel is False, \
            'Should filter all channels by is_channel false'


async def test_filter_channel_by_timestamp(channel_data):
    date = datetime.now() - timedelta(days=2920)

    # Filter timestamp start
    channels = await messaging_context.channel_query().filter_by_timestamp(
        start=date).filter()

    for channel in channels:
        assert channel.timestamp > date, \
            'Should filter channel by start timestamp'

    # Filter timestamp end
    channels = await messaging_context.channel_query().filter_by_timestamp(
        end=date).filter()

    for channel in channels:
        assert channel.timestamp < date, \
            'Should filter channel by end timestamp'

    # Filter timestamp start and end
    start = date
    end = datetime.now() - timedelta(days=365)

    channels = await messaging_context.channel_query().filter_by_timestamp(
        start=start, end=end).filter()

    for channel in channels:
        assert channel.timestamp < end and \
            channel.timestamp > start, \
            'Should filter channel by start and end timestamp'


async def test_filter_channel_by_edited_timestamp(channel_data):
    date = datetime.now() - timedelta(days=2920)

    # Filter edited_timestamp start
    channels = await messaging_context.channel_query(
        ).filter_by_edited_timestamp(start=date).filter()

    for channel in channels:
        assert channel.edited_timestamp > date, \
            'Should filter channel by start edited timestamp'

    # Filter edited timestamp end
    channels = await messaging_context.channel_query(
        ).filter_by_edited_timestamp(end=date).filter()

    for channel in channels:
        assert channel.edited_timestamp < date, \
            'Should filter channel by end edited timestamp'

    # Filter edited timestamp start and end
    start = date
    end = datetime.now() - timedelta(days=365)

    channels = await messaging_context.channel_query(
        ).filter_by_edited_timestamp(start=start, end=end).filter()

    for channel in channels:
        assert channel.edited_timestamp < end and \
            channel.edited_timestamp > start, \
            'Should filter channel by start and end edited timestamp'
