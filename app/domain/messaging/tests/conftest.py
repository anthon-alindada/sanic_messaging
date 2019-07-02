# -*- coding: utf-8
# Core
import pytest
import random
from datetime import datetime
from mixer.main import mixer

# App
from app import create_app


app = create_app('test')


class ChannelFactory:
    id = int
    owner_id = int
    name = str
    is_channel = bool
    timestamp = datetime
    edited_timestamp = datetime


class MessageFactory:
    id = int
    content = str
    author_id = int
    channel_id = int
    timestamp = datetime
    edited_timestamp = datetime


@pytest.fixture
def sanic_server(loop, test_server):
    return loop.run_until_complete(test_server(app))


def pytest_namespace():
    return {
        'channels_data': None,
        'messages_data': None,
    }


@pytest.fixture
def channel_data(loop, sanic_server, request):
    """
    Initial channel domain test
    """
    # Models
    from ..models import Channel, ChannelUser

    if pytest.channels_data is None:
        # Delete all channels data in database
        loop.run_until_complete(Channel.delete.gino.status())

        channels_data = []

        # Generate fixed channel
        channel_instance = loop.run_until_complete(Channel.create(
            id=1,
            owner_id=1,
            name='General'))

        channels_data.append(channel_instance)

        # Add user to channel default
        loop.run_until_complete(ChannelUser.create(
            channel_id=channel_instance.id, user_id=1))

        # Generate fixed channel
        channel_instance = loop.run_until_complete(Channel.create(
            id=2,
            owner_id=1,
            name='General'))

        channels_data.append(channel_instance)

        # Generate random channels
        channels = mixer.cycle(10).blend(ChannelFactory)

        for channel in channels:
            channel_instance = loop.run_until_complete(Channel.create(
                owner_id=1,
                name=channel.name,
                is_channel=channel.is_channel,
                timestamp=channel.timestamp,
                edited_timestamp=channel.edited_timestamp))

            channels_data.append(channel_instance)

            # Generate random channel user data
            if random.choice([True, False]):
                loop.run_until_complete(ChannelUser.create(
                    channel_id=channel_instance.id, user_id=1))

        pytest.channels_data = channels_data

    return pytest.channels_data


@pytest.fixture
def message_data(loop, sanic_server, request, channel_data):
    """
    Initial message domain test
    """
    # Models
    from ..models import Message

    if pytest.messages_data is None:
        # Delete all users data in database
        loop.run_until_complete(Message.delete.gino.status())

        messages_data = []
        channel = channel_data[0]

        # Generate fixed messages
        message_instance = loop.run_until_complete(Message.create(
            id=1,
            content="sample content",
            author_id=1,
            channel_id=channel.id))

        messages_data.append(message_instance)

        # Generate random messages
        messages = mixer.cycle(10).blend(MessageFactory)

        for message in messages:
            channel = random.choice(channel_data)

            message_instance = loop.run_until_complete(Message.create(
                content=message.content,
                author_id=1,
                channel_id=channel.id,
                timestamp=channel.timestamp,
                edited_timestamp=channel.edited_timestamp))

            messages_data.append(message_instance)

        pytest.messages_data = messages_data

    return pytest.messages_data
