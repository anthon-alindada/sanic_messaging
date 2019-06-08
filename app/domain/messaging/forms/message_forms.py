# -*- coding: utf-8
# Core
from sanic_wtf import SanicForm
from wtforms import StringField, validators, ValidationError


class CreateMessageForm(SanicForm):
    """
    Create message form
    """

    content = StringField('Content', validators=[
        validators.DataRequired(
            message='Content is required',
        ),
        validators.Length(
            max=255,
            message='Content must be less than or equal to 255 characters',
        ),
    ])


class UpdateMessageForm(SanicForm):
    """
    Update message form
    """

    _message_instance = None

    _author_id = None

    content = StringField('Content', validators=[
        validators.DataRequired(
            message='Content is required',
        ),
        validators.Length(
            max=255,
            message='Content must be less than or equal to 255 characters',
        ),
    ])

    async def set_author_id(self, author_id):
        """
        Set author_id that updates the channel
        """
        self._author_id = author_id

    async def set_message_instance(self, message_instance):
        """
        Set message instance to update
        """
        self._message_instance = message_instance

    def validate_content(self, content):
        if self._message_instance is not None:
            # Compare author_id
            if self._message_instance.author_id != self._author_id:
                raise ValidationError('Unauthorized to update message')

        return content
