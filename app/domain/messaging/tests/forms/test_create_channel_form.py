# -*- coding: utf-8
# Messaging context
from ... import messaging_context


async def test_create_channel_form_name(channel_data):
    # Validate blank name
    create_channel_form = messaging_context.create_channel_form()(
        data={'name': ''})

    create_channel_form.validate()

    assert create_channel_form.errors.get(
        'name') == ['Name is required'], \
        'Should be invalid if name is blank'

    # Validate long name
    create_channel_form = messaging_context.create_channel_form()(
        data={
            'name': 'sdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdla'})

    create_channel_form.validate()

    assert create_channel_form.errors.get(
        'name') == ['Name must be less than or equal to 50 characters'], \
        'Should be invalid if name is morethan 22'

    # Validate correct name
    create_channel_form = messaging_context.create_channel_form()(
        data={'name': 'Channel name'})

    create_channel_form.validate()

    assert create_channel_form.errors.get('name') is None, \
        'Should be a valid name'
