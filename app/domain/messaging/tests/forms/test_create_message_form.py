# -*- coding: utf-8
# Messaging context
from ... import messaging_context


async def test_create_message_form_content(message_data):
    # Validate blank content
    create_message_form = messaging_context.create_message_form()(
        data={'content': ''})

    create_message_form.validate()

    assert create_message_form.errors.get(
        'content') == ['Content is required'], \
        'Should be invalid if content is blank'

    # Validate long content
    create_message_form = messaging_context.create_message_form()(
        data={
            'content': 'sdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdlsdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdlsdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdlaaasdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdlasdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdlsdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdlsdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdlaaasdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdla'})  # noqa

    create_message_form.validate()

    assert create_message_form.errors.get(
        'content') == ['Content must be less than or equal to 255 characters'], 'Should be invalid if message is morethan 225'  # noqa

    # Validate correct content
    create_message_form = messaging_context.create_message_form()(
        data={'content': 'This is a message'})

    create_message_form.validate()

    assert create_message_form.errors.get('content') is None, \
        'Should be a valid content'
