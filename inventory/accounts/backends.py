# -*- coding: utf-8 -*-
#
# realm/common/backends.py
#

"""
Authentication backends.
"""
__docformat__ = "restructuredtext en"

from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import RemoteUserBackend

UserModel = get_user_model()


class RealmRemoteUserBackend(RemoteUserBackend):
    """
    We override the Django RemoteUserBackend so we can create an email
    and hit AD to get the users full name.
    """

    def authenticate(self, request, remote_user):
        """
        The username passed as ``remote_user`` is considered trusted. Return
        the ``User`` object with the given username. Create a new ``User``
        object if ``create_unknown_user`` is ``True``.

        Return None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        user = None

        if remote_user:
            username = self.clean_username(remote_user)
            first_name = request.META.get('HTTP_USER_GIVEN_NAME', '')
            last_name = request.META.get('HTTP_USER_FAMILY_NAME', '')
            email = request.META.get('HTTP_USER_EMAIL', '')

            # Note that this could be accomplished in one try-except clause,
            # but instead we use get_or_create when creating unknown users
            # since it has built-in safeguards for multiple threads.
            if self.create_unknown_user:
                defaults = {
                    'first_name': first_name.strip(),
                    'last_name': last_name.strip(),
                    'email': email.strip(),
                    'password': uuid4()
                    }
                user, created = UserModel._default_manager.get_or_create(
                    **{UserModel.USERNAME_FIELD: username}, defaults=defaults)
            else:
                try:
                    user = UserModel._default_manager.get_by_natural_key(
                        username)
                except UserModel.DoesNotExist:
                    pass
                else:
                    user = user if self.user_can_authenticate(user) else None

        return user
