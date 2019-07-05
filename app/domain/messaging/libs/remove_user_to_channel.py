# -*- coding: utf-8
# Core
from sanic_wtf import SanicForm
from wtforms import StringField, validators, ValidationError

# Exception
from ..exceptions import InvalidInput


class RemoveUserToChannelValidator(SanicForm):
    """
    Remove user to channel form
    """

    user_id = StringField('user_id', validators=[
        validators.DataRequired(
            message='user_id is required',
        ),
    ])

    def validate_user_id(self, user_id):
        if user_id.data is not None:
            try:
                int(user_id.data)
            except (ValueError, TypeError):
                raise ValidationError('user_id is invalid')

        return user_id


class RemoveUserToChannel:
    """
    Remove user to channel library
    """

    def __init__(self, channel_store, channel_user_query):
        # Library
        self.channel_store = channel_store
        self.channel_user_query = channel_user_query

        # Errors
        self._errors = {}

    async def validate(self, channel_instance, user_id) -> bool:
        """
        Validate input data
        """

        # Validate remove user to channel form input
        remove_user_to_channel_validator = RemoveUserToChannelValidator(data={
            'user_id': user_id,
        })

        if remove_user_to_channel_validator.validate() is False:
            # Set errors
            self._errors = remove_user_to_channel_validator.errors

        # Check if user is added to channel
        if self._errors.get('user_id', None) is None:
            self.channel_user = await self.channel_user_query.find_by_id(
                channel_id=channel_instance.id, user_id=user_id).find()

            if self.channel_user is None:
                await self.set_error('user_id', 'user does not exist')

        # If errors exist
        if self._errors:
            return False

        return True

    async def set_error(self, field, message) -> None:
        """
        Set error field
        """
        self._errors[field] = [message]

    async def run(self, channel_instance, user_id):
        """
        Run the service
        """

        # Validate input
        is_valid = await self.validate(channel_instance, user_id)

        if is_valid is False:
            raise InvalidInput(self._errors)

        # Remove user to channel
        await self.channel_store.remove_user(channel_user=self.channel_user)

        return True

    async def get_errors(self):
        """
        Get errors
        """
        return self._errors
