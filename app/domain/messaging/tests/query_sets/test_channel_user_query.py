# -*- coding: utf-8
# Models
from app.domain.messaging.models import ChannelUser

# Messaging context
from ... import messaging_context


async def test_find_channel_user_by_id(channel_data):
    channel_user = await messaging_context.channel_user_query().find_by_id(
        channel_id=28239, user_id=123).find()

    assert channel_user is None, 'Should return None if id does not exist'

    channel_user = await messaging_context.channel_user_query().find_by_id(
        channel_id=1, user_id=1).find()

    assert isinstance(channel_user, ChannelUser), 'Should get channel by id'
