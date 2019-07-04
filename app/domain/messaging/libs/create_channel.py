# -*- coding: utf-8
# Core
from sanic_wtf import SanicForm
from wtforms import StringField, validators

# Exception
from ..exceptions import InvalidInput


class CreateChannelValidator(SanicForm):
    """
    Create channel form
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


class CreateChannel:
    """
    Crate channel library
    """

    def __init__(self, channel_store):
        # Library
        self.channel_store = channel_store

        # Errors
        self._errors = {}

    async def validate(self, name) -> bool:
        """
        Validate input data
        """

        # Validate create channel form input
        create_channel_validator = CreateChannelValidator(data={
            'name': name,
        })

        if create_channel_validator.validate() is False:
            # Set errors
            self._errors = create_channel_validator.errors

        # If errors exist
        if self._errors:
            return False

        return True

    async def run(self, name, owner_id, is_channel):
        """
        Run the service
        """

        # Validate input
        is_valid = await self.validate(name)

        if is_valid is False:
            raise InvalidInput(self._errors)

        # Create new channel
        channel = await self.channel_store.create(
            owner_id=owner_id,
            name=name,
            is_channel=is_channel)

        return channel

    async def get_errors(self):
        """
        Get errors
        """
        return self._errors
