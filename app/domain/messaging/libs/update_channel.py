# -*- coding: utf-8
# Core
from sanic_wtf import SanicForm
from wtforms import StringField, validators

# Exception
from ..exceptions import InvalidInput


class UpdateChannelValidator(SanicForm):
    """
    Update channel form
    """

    name = StringField('Name', validators=[
        validators.DataRequired(
            message='Name is required',
        ),
        validators.Length(
            max=50,
            message='Name must be less than or equal to 50 characters',
        ),
    ])


class UpdateChannel:
    """
    Update channel library
    """

    def __init__(self, channel_store):
        # Library
        self.channel_store = channel_store

        # Errors
        self._errors = {}

    async def validate(self, channel_instance, owner_id, name) -> bool:
        """
        Validate input data
        """

        # Validate update channel form input
        update_channel_validator = UpdateChannelValidator(data={
            'name': name,
        })

        if update_channel_validator.validate() is False:
            # Set errors
            self._errors = update_channel_validator.errors

        # Check if channel is_channel is false
        if self._errors.get('name', None) is None:
            if channel_instance.is_channel is False:
                await self.set_error('name', 'Cannot update channel')

        # Compare owner_id
        if self._errors.get('name', None) is None:
            if channel_instance.owner_id != owner_id:
                await self.set_error('name', 'Unauthorized to update channel')

        # If errors exist
        if self._errors:
            return False

        return True

    async def set_error(self, field, message) -> None:
        """
        Set error field
        """
        self._errors[field] = [message]

    async def run(self, channel_instance, name, owner_id):
        """
        Run the service
        """

        # Validate input
        is_valid = await self.validate(channel_instance, owner_id, name)

        if is_valid is False:
            raise InvalidInput(self._errors)

        # Update channel
        channel = await self.channel_store.set_name(
            channel=channel_instance, name=name)

        return channel

    async def get_errors(self):
        """
        Get errors
        """
        return self._errors
