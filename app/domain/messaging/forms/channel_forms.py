# -*- coding: utf-8
# Core
from sanic_wtf import SanicForm
from wtforms import StringField, validators, ValidationError


class CreateChannelForm(SanicForm):
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


class UpdateChannelForm(SanicForm):
    """
    Update channel form
    """

    _channel_instance = None

    _owner_id = None

    name = StringField('Name', validators=[
        validators.DataRequired(
            message='Name is required',
        ),
        validators.Length(
            max=50,
            message='Name must be less than or equal to 50 characters',
        ),
    ])

    async def set_owner_id(self, owner_id):
        """
        Set owner_id that updates the channel
        """
        self._owner_id = owner_id

    async def set_channel_instance(self, channel_instance):
        """
        Set channel instance to update
        """
        self._channel_instance = channel_instance

    def validate_name(self, name):
        if self._channel_instance is not None:
            # Check if channel is_channel is false
            if self._channel_instance.is_channel is False:
                raise ValidationError('Cannot update channel')

            # Compare owner_id
            if self._channel_instance.owner_id != self._owner_id:
                raise ValidationError('Unauthorized to update channel')

        return name
