# -*- coding: utf-8
# Messaging context
from ... import messaging_context


async def test_update_channel_form_name(channel_data):
    # Validate blank name
    update_channel_form = messaging_context.update_channel_form()(
        data={'name': ''})

    update_channel_form.validate()

    assert update_channel_form.errors.get(
        'name') == ['Name is required'], \
        'Should be invalid if name is blank'

    # Validate long name
    update_channel_form = messaging_context.update_channel_form()(
        data={
            'name': 'sdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdla'})

    update_channel_form.validate()

    assert update_channel_form.errors.get(
        'name') == ['Name must be less than or equal to 50 characters'], \
        'Should be invalid if name is morethan 22'

    # Get channel instance
    channel_instance = None
    for channel in channel_data:
        if channel.is_channel is False:
            channel_instance = channel
            break

    # Cannot update if is_channel is False
    update_channel_form = messaging_context.update_channel_form()(
        data={'name': 'updated name'})

    await update_channel_form.set_channel_instance(channel_instance)

    update_channel_form.validate()

    assert update_channel_form.errors.get(
        'name') == ['Cannot update channel'], \
        'Should be invalid if channel is_channel is False'

    # Validate not owner
    update_channel_form = messaging_context.update_channel_form()(
        data={'name': 'updated name'})

    await update_channel_form.set_channel_instance(channel_data[0])
    await update_channel_form.set_owner_id(2)

    update_channel_form.validate()

    assert update_channel_form.errors.get(
        'name') == ['Unauthorized to update channel'], \
        'Should be invalid if channel owner is not the same'

    # Validate correct name
    update_channel_form = messaging_context.update_channel_form()(
        data={'name': 'updated name'})

    await update_channel_form.set_channel_instance(channel_data[0])
    await update_channel_form.set_owner_id(channel_instance.owner_id)

    update_channel_form.validate()

    assert update_channel_form.errors.get('name') is None, \
        'Should be a valid name'
