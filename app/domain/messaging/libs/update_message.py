# -*- coding: utf-8
# Core
from sanic_wtf import SanicForm
from wtforms import StringField, validators

# Exception
from ..exceptions import InvalidInput


class UpdateMessageValidator(SanicForm):
    """
    Update message form
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


class UpdateMessage:
    """
    Update message library
    """

    def __init__(self, message_store):
        # Library
        self.message_store = message_store

        # Errors
        self._errors = {}

    async def validate(self, message_instance, content, author_id) -> bool:
        """
        Validate input data
        """

        # Validate update message form input
        update_message_validator = UpdateMessageValidator(data={
            'content': content,
        })

        if update_message_validator.validate() is False:
            # Set errors
            self._errors = update_message_validator.errors

        # Compare author_id
        if self._errors.get('content', None) is None:
            if message_instance.author_id != author_id:
                await self.set_error(
                    'content', 'Unauthorized to update message')

        # If errors exist
        if self._errors:
            return False

        return True

    async def set_error(self, field, message) -> None:
        """
        Set error field
        """
        self._errors[field] = [message]

    async def run(self, message_instance, content, author_id):
        """
        Run the service
        """

        # Validate input
        is_valid = await self.validate(
            message_instance=message_instance,
            content=content,
            author_id=author_id)

        if is_valid is False:
            raise InvalidInput(self._errors)

        # Update message
        message = await self.message_store.set_content(
            message=message_instance, content=content)

        return message

    async def get_errors(self):
        """
        Get errors
        """
        return self._errors
