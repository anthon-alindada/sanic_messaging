# -*- coding: utf-8
# Core
from distutils.util import strtobool
from datetime import datetime


# Exception
from ..exceptions import InvalidInput, NotFound


class FilterChannel:
    """
    Filter Channel library
    """

    def __init__(self, channel_query):
        # Query set
        self.channel_query = channel_query

        # Errors
        self._errors = {}

    async def validate(self) -> bool:
        """
        Validate input data
        """

        # Validate owner_id
        if self._errors.get('owner_id', None) is None and \
           self.owner_id is not None:
            try:
                self.owner_id = int(self.owner_id)
            except (ValueError, TypeError):
                await self.set_error('owner_id', 'owner_id is invalid')

        # Validate user_id
        if self._errors.get('user_id', None) is None and \
           self.user_id is not None:
            try:
                self.user_id = int(self.user_id)
            except (ValueError, TypeError):
                await self.set_error('user_id', 'user_id is invalid')

        # Validate is_channel
        if self._errors.get('user_id', None) is None and \
           self.is_channel is not None:
            if str(self.is_channel).lower() not in ['true', 'false']:
                await self.set_error('is_channel', 'is_channel is invalid')

        # Validate timestamp_start
        if self.timestamp_start is not None:
            try:
                self.timestamp_start = datetime.fromtimestamp(
                    int(self.timestamp_start))
            except (ValueError, TypeError):
                await self.set_error(
                    'timestamp_start', 'timestamp_start is invalid')

        # Validate timestamp_end
        if self.timestamp_end is not None:
            try:
                self.timestamp_end = datetime.fromtimestamp(
                    int(self.timestamp_end))
            except (ValueError, TypeError):
                await self.set_error(
                    'timestamp_end', 'timestamp_end is invalid')

        # Validate edited_timestamp_start
        if self.edited_timestamp_start is not None:
            try:
                self.edited_timestamp_start = datetime.fromtimestamp(
                    int(self.edited_timestamp_start))
            except (ValueError, TypeError):
                await self.set_error(
                    'edited_timestamp_start',
                    'edited_timestamp_start is invalid')

        # Validate edited_timestamp_end
        if self.edited_timestamp_end is not None:
            try:
                self.edited_timestamp_end = datetime.fromtimestamp(
                    int(self.edited_timestamp_end))
            except (ValueError, TypeError):
                self._errors['edited_timestamp_end'] = \
                    'edited_timestamp_end is invalid'
                await self.set_error(
                    'edited_timestamp_end',
                    'edited_timestamp_end is invalid')

        # Validate channel_id
        if self.channel_id is not None:
            try:
                self.channel_id = int(self.channel_id)
            except (ValueError, TypeError):
                await self.set_error('channel_id', 'channel_id is invalid')

        # If errors exist
        if self._errors:
            return False

    async def set_error(self, field, message) -> None:
        """
        Set error field
        """
        self._errors[field] = [message]

    async def run(
        self,
        owner_id=None,
        user_id=None,
        is_channel=None,
        timestamp_start=None,
        timestamp_end=None,
        edited_timestamp_start=None,
        edited_timestamp_end=None,
        channel_id=None,
    ):
        """
        Run the service
        """

        # Set inputs
        self.owner_id = owner_id
        self.user_id = user_id
        self.is_channel = is_channel
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end
        self.edited_timestamp_start = edited_timestamp_start
        self.edited_timestamp_end = edited_timestamp_end
        self.channel_id = channel_id

        # Validate input
        is_valid = await self.validate()

        if is_valid is False:
            raise InvalidInput(self._errors)

        channel_query = self.channel_query

        # Filter owner_id
        if self.owner_id is not None:
            channel_query = channel_query.filter_by_owner_id(self.owner_id)

        # Filter user_id
        if self.user_id is not None:
            channel_query = channel_query.filter_by_user_id(self.user_id)

        # Filter is_channel
        if self.is_channel is not None:
            channel_query = channel_query.filter_by_is_channel(
                bool(strtobool(self.is_channel)))

        # Filter timestamp start and end
        channel_query = channel_query.filter_by_timestamp(
            start=self.timestamp_start,
            end=self.timestamp_end)

        # Filter timestamp start and end
        channel_query = channel_query.filter_by_edited_timestamp(
            start=self.edited_timestamp_start,
            end=self.edited_timestamp_end)

        # Find by channel_id
        if self.channel_id is not None:
            channel = await channel_query.find_by_id(
                id=int(self.channel_id)).find()

            if channel is None:
                raise NotFound

            # Return channel if found by id
            return channel

        return await channel_query.filter()

    async def get_errors(self):
        """
        Get errors
        """
        return self._errors
