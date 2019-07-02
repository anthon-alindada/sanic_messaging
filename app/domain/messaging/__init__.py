# -*- coding: utf-8

# Dependency injector
from dependency_injector import containers
from dependency_injector import providers


app = None
db = None


# Messaging context
messaging_context = containers.DynamicContainer()


def init_messaging_app(
    app_instance,
    db_instance,
):
    global app
    global db

    app = app_instance
    db = db_instance

    # Stores
    from .stores.channel_store import ChannelStore
    from .stores.message_store import MessageStore

    # Query sets
    from .query_sets.channel_query import ChannelQuery
    from .query_sets.message_query import MessageQuery

    # Forms
    from .forms.channel_forms import CreateChannelForm, UpdateChannelForm
    from .forms.message_forms import CreateMessageForm, UpdateMessageForm

    # Libs
    from .libs.create_channel import CreateChannel
    from .libs.create_message import CreateMessage
    from .libs.filter_channel import FilterChannel
    from .libs.filter_message import FilterMessage
    from .libs.update_channel import UpdateChannel
    from .libs.update_message import UpdateMessage
    from .libs.add_user_to_channel import AddUserToChannel

    # Set messaging context
    # Set dependency injector providers
    # Stores
    messaging_context.channel_store = providers.Singleton(ChannelStore)
    messaging_context.message_store = providers.Singleton(MessageStore)

    # Query sets
    messaging_context.channel_query = providers.Factory(ChannelQuery)
    messaging_context.message_query = providers.Factory(MessageQuery)

    # Forms
    messaging_context.create_channel_form = providers.Object(CreateChannelForm)
    messaging_context.update_channel_form = providers.Object(UpdateChannelForm)
    messaging_context.create_message_form = providers.Object(CreateMessageForm)
    messaging_context.update_message_form = providers.Object(UpdateMessageForm)

    # Libs
    messaging_context.create_channel = providers.Factory(
        CreateChannel,
        create_channel_form=messaging_context.create_channel_form,
        channel_store=messaging_context.channel_store)
    messaging_context.create_message = providers.Factory(
        CreateMessage,
        create_message_form=messaging_context.create_message_form,
        message_store=messaging_context.message_store)
    messaging_context.filter_channel = providers.Factory(
        FilterChannel,
        channel_query=messaging_context.channel_query)
    messaging_context.filter_message = providers.Factory(
        FilterMessage,
        message_query=messaging_context.message_query)
    messaging_context.update_channel = providers.Factory(
        UpdateChannel,
        update_channel_form=messaging_context.update_channel_form,
        channel_store=messaging_context.channel_store)
    messaging_context.update_message = providers.Factory(
        UpdateMessage,
        update_message_form=messaging_context.update_message_form,
        message_store=messaging_context.message_store)
    messaging_context.add_user_to_channel = providers.Factory(
        AddUserToChannel,
        channel_store=messaging_context.channel_store,
        channel_query=messaging_context.channel_query)
