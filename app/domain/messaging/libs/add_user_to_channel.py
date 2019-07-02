# -*- coding: utf-8
# Core
from marshmallow import Schema, fields

# Exception
from ..exceptions import InvalidInput


class ValidatorSchema(Schema):
    """
    Marshmallow schema validator
    """

    user_id = fields.Int(
        required=True,
        error_messages={
            'invalid': 'user_id is invalid',
            'required': 'user_id is required',
            'null': 'user_id is required',
        })


class AddUserToChannel:
    """
    Add user to channel library
    """

    def __init__(self, channel_store, channel_query):
        # Library
        self.channel_store = channel_store
        self.channel_query = channel_query

        # Errors
        self._errors = {}

    async def validate(self, channel_instance, user_id) -> bool:
        """
        Validate input data
        """

        # Validate schema
        _, errors = ValidatorSchema().load({
            'user_id': user_id})

        if errors:
            # Set errors
            # Get first value in array in marshmallow
            self._errors = dict(map(lambda t: (t[0], t[1][0]), errors.items()))

        # Check if user_id already added
        if self._errors.get('user_id', None) is None:
            channel_user = await self.channel_query.filter_by_user_id(
                user_id=user_id).find_by_id(channel_instance.id).find()

            # If channel_user exist set error
            if channel_user is not None:
                await self.set_error('user_id', 'user_id already added')

        # If errors exist
        if self._errors:
            return False

        return True

    async def set_error(self, field, message) -> None:
        """
        Set error field
        """
        self._errors[field] = message

    async def run(self, channel_instance, user_id):
        """
        Run the service
        """

        # Validate input
        is_valid = await self.validate(
            channel_instance=channel_instance, user_id=user_id)

        if is_valid is False:
            raise InvalidInput(self._errors)

        # Add user to channel
        channel_user = await self.channel_store.add_user(
            channel_id=channel_instance.id, user_id=user_id)

        return channel_user

    async def get_errors(self):
        """
        Get errors
        """
        return self._errors
