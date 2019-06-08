# -*- coding: utf-8
# Messaging context
from ... import messaging_context


async def test_update_message_form_name(message_data):
    # Validate blank name
    update_message_form = messaging_context.update_message_form()(
        data={'content': ''})

    update_message_form.validate()

    assert update_message_form.errors.get(
        'content') == ['Content is required'], \
        'Should be invalid if content is blank'

    # Validate long content
    update_message_form = messaging_context.update_message_form()(
        data={
            'content': 'sdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdlsdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdlsdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdlaaasdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdlasdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdlsdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdlsdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdlaaasdfsjdlfjsdlkjfksdjlfjsdlkfjsldjflksdjfjsdlfjsdlkjsdla'})  # noqa

    update_message_form.validate()

    assert update_message_form.errors.get(
        'content') == ['Content must be less than or equal to 255 characters'], 'Should be invalid if message is morethan 225'  # noqa

    # Validate not author
    update_message_form = messaging_context.update_message_form()(
        data={'content': 'Updated content'})

    await update_message_form.set_message_instance(message_data[0])
    await update_message_form.set_author_id(1232)

    update_message_form.validate()

    assert update_message_form.errors.get(
        'content') == ['Unauthorized to update message'], \
        'Should be invalid if message author is not the same'

    # Validate correct content
    update_message_form = messaging_context.update_message_form()(
        data={'content': 'updated content'})

    await update_message_form.set_message_instance(message_data[0])
    await update_message_form.set_author_id(message_data[0].author_id)

    update_message_form.validate()

    assert update_message_form.errors.get('content') is None, \
        'Should be a valid name'
