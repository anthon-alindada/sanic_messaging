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

    async def run(
        self,
        owner_id=None,
        is_channel=None,
        timestamp_start=None,
        timestamp_end=None,
        edited_timestamp_start=None,
        edited_timestamp_end=None,
        channel_id=None,
    ):
        # Set inputs
        self.owner_id = owner_id
        self.is_channel = is_channel
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end
        self.edited_timestamp_start = edited_timestamp_start
        self.edited_timestamp_end = edited_timestamp_end
        self.channel_id = channel_id

        # Validate inputs
        is_valid = await self.validate_inputs()

        if is_valid is False:
            raise InvalidInput

        channel_query = self.channel_query

        # Filter owner_id
        if self.owner_id is not None:
            channel_query = channel_query.filter_by_owner_id(self.owner_id)

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

    async def validate_inputs(self):
        # Validate owner_id
        if self.owner_id is not None:
            try:
                self.owner_id = int(self.owner_id)
            except (ValueError, TypeError):
                self._errors['owner_id'] = 'owner_id is invalid'

        # Validate is_channel
        if self.is_channel is not None:
            if str(self.is_channel).lower() not in ['true', 'false']:
                self._errors['is_channel'] = 'is_channel is invalid'

        # Validate timestamp_start
        if self.timestamp_start is not None:
            try:
                self.timestamp_start = datetime.fromtimestamp(
                    int(self.timestamp_start))
            except (ValueError, TypeError):
                self._errors['timestamp_start'] = 'timestamp_start is invalid'

        # Validate timestamp_end
        if self.timestamp_end is not None:
            try:
                self.timestamp_end = datetime.fromtimestamp(
                    int(self.timestamp_end))
            except (ValueError, TypeError):
                self._errors['timestamp_end'] = 'timestamp_end is invalid'

        # Validate edited_timestamp_start
        if self.edited_timestamp_start is not None:
            try:
                self.edited_timestamp_start = datetime.fromtimestamp(
                    int(self.edited_timestamp_start))
            except (ValueError, TypeError):
                self._errors['edited_timestamp_start'] = \
                    'edited_timestamp_start is invalid'

        # Validate edited_timestamp_end
        if self.edited_timestamp_end is not None:
            try:
                self.edited_timestamp_end = datetime.fromtimestamp(
                    int(self.edited_timestamp_end))
            except (ValueError, TypeError):
                self._errors['edited_timestamp_end'] = \
                    'edited_timestamp_end is invalid'

        # Validate channel_id
        if self.channel_id is not None:
            try:
                self.channel_id = int(self.channel_id)
            except (ValueError, TypeError):
                self._errors['channel_id'] = 'channel_id is invalid'

        return not self._errors

    async def get_errors(self):
        return self._errors
