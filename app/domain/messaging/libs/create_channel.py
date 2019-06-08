# -*- coding: utf-8
# Exception
from ..exceptions import InvalidInput


class CreateChannel:
    """
    Crate channel library
    """

    def __init__(
        self,
        create_channel_form,
        channel_store,
    ):
        # Library
        self.create_channel_form = create_channel_form
        self.channel_store = channel_store

        # Errors
        self._errors = {}

    async def run(self, name, owner_id, is_channel):
        # Validate create channel form
        create_channel_form = self.create_channel_form(data={
            'name': name,
        })

        if create_channel_form.validate() is False:
            self._errors = create_channel_form.errors
            raise InvalidInput

        # Create new channel
        channel = await self.channel_store.create(
            owner_id=owner_id,
            name=name,
            is_channel=is_channel)

        return channel

    async def get_errors(self):
        return self._errors
