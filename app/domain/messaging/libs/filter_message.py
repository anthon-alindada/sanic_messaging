# -*- coding: utf-8
# Core
from datetime import datetime

# Exception
from ..exceptions import InvalidInput, NotFound


class FilterMessage:
    """
    Filter Message library
    """

    def __init__(self, message_query):
        # Query set
        self.message_query = message_query

        # Errors
        self._errors = {}

    async def validate(self) -> bool:
        """
        Validate input data
        """

        # Validate message_id
        if self.message_id is not None:
            try:
                self.message_id = int(self.message_id)
            except (ValueError, TypeError):
                await self.set_error('message_id', 'message_id is invalid')

        # Validate author_id
        if self.author_id is not None:
            try:
                self.author_id = int(self.author_id)
            except (ValueError, TypeError):
                await self.set_error('author_id', 'author_id is invalid')

        # Validate channel_id
        if self.channel_id is not None:
            try:
                self.channel_id = int(self.channel_id)
            except (ValueError, TypeError):
                await self.set_error('channel_id', 'channel_id is invalid')

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
                await self.set_error(
                    'edited_timestamp_end',
                    'edited_timestamp_end is invalid')

        return not self._errors

    async def set_error(self, field, message) -> None:
        """
        Set error field
        """
        self._errors[field] = [message]

    async def run(
        self,
        message_id=None,
        author_id=None,
        channel_id=None,
        timestamp_start=None,
        timestamp_end=None,
        edited_timestamp_start=None,
        edited_timestamp_end=None,
    ):
        """
        Run the service
        """

        # Set inputs
        self.message_id = message_id
        self.author_id = author_id
        self.channel_id = channel_id
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end
        self.edited_timestamp_start = edited_timestamp_start
        self.edited_timestamp_end = edited_timestamp_end

        # Validate input
        is_valid = await self.validate()

        if is_valid is False:
            raise InvalidInput(self._errors)

        message_query = self.message_query

        # Filter author_id
        if self.author_id is not None:
            message_query = message_query.filter_by_author_id(self.author_id)

        # Filter channel_id
        if self.channel_id is not None:
            message_query = message_query.filter_by_channel_id(self.channel_id)

        # Filter timestamp start and end
        message_query = message_query.filter_by_timestamp(
            start=self.timestamp_start,
            end=self.timestamp_end)

        # Filter timestamp start and end
        message_query = message_query.filter_by_edited_timestamp(
            start=self.edited_timestamp_start,
            end=self.edited_timestamp_end)

        # Find message by id
        if self.message_id is not None:
            message = await message_query.find_by_id(self.message_id).find()

            # Raise not found if None
            if message is None:
                raise NotFound

            return message

        return await message_query.filter()

    async def get_errors(self):
        """
        Get errors
        """
        return self._errors
