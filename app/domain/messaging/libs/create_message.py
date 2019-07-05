# -*- coding: utf-8
# Core
from sanic_wtf import SanicForm
from wtforms import StringField, validators

# Exception
from ..exceptions import InvalidInput


class CreateMessageValidator(SanicForm):
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


class CreateMessage:
    """
    Crate message library
    """

    def __init__(self, message_store):
        # Library
        self.message_store = message_store

        # Errors
        self._errors = {}

    async def validate(self, content) -> bool:
        """
        Validate input data
        """

        # Validate create message form input
        create_message_validator = CreateMessageValidator(data={
            'content': content,
        })

        if create_message_validator.validate() is False:
            # Set errors
            self._errors = create_message_validator.errors

        # If errors exist
        if self._errors:
            return False

        return True

    async def run(self, content, author_id, channel_id):
        """
        Run the service
        """

        # Validate input
        is_valid = await self.validate(content)

        if is_valid is False:
            raise InvalidInput(self._errors)

        # Create new message
        message = await self.message_store.create(
            author_id=author_id,
            channel_id=channel_id,
            content=content)

        return message

    async def get_errors(self):
        """
        Get errors
        """
        return self._errors
