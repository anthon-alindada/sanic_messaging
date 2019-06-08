# -*- coding: utf-8
# Exception
from ..exceptions import InvalidInput


class UpdateChannel:
    """
    Update channel library
    """

    def __init__(
        self,
        update_channel_form,
        channel_store,
    ):
        # Library
        self.update_channel_form = update_channel_form
        self.channel_store = channel_store

        # Errors
        self._errors = {}

    async def run(self, channel_instance, name, owner_id):
        # Validate update channel form
        update_channel_form = self.update_channel_form(data={
            'name': name,
        })

        await update_channel_form.set_channel_instance(channel_instance)
        await update_channel_form.set_owner_id(owner_id)

        if update_channel_form.validate() is False:
            self._errors = update_channel_form.errors
            raise InvalidInput

        # Update channel
        channel = await self.channel_store.set_name(
            channel=channel_instance, name=name)

        return channel

    async def get_errors(self):
        return self._errors
