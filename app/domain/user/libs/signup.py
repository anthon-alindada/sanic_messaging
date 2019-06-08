# -*- coding: utf-8
# Exception
from ..exceptions import InvalidInput


class Signup:
    """
    Signup
    """

    def __init__(
        self,
        user_query,
        signup_form,
        user_store,
    ):
        # Library
        self.user_query = user_query
        self.signup_form = signup_form
        self.user_store = user_store

        # Errors
        self._errors = {}

    async def run(self, first_name, last_name, email,
                  password, confirm_password):
        # Set user query active
        user_query_active = self.user_query.new()

        # Get active user with same email
        user = await user_query_active.filter_by_active(
            ).find_by_email(email).find()

        # Validate signup form
        signup_form = self.signup_form(data={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
        })

        # Signup form set existing user
        signup_form.set_existing_user(user=user)

        # Validate signup form
        if signup_form.validate() is False:
            self._errors = signup_form.errors
            raise InvalidInput

        # Set user query inactive
        user_query_inactive = self.user_query.new()

        # Get inactive user with same email
        user = await user_query_inactive.filter_by_inactive(
            ).find_by_email(email).find()

        if user is not None:
            # Delete existing inactive user
            await user.delete()

        # Create new inactive user
        user = await self.user_store.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password)

        # Activate user
        user = await self.user_store.activate(user=user)
        await self.user_store.save()

        return user

    async def get_errors(self):
        return self._errors
