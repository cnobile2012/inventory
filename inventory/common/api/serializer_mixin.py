#
# inventory/common/api/serializer_mixin.py
#

from django.contrib.auth import get_user_model

User = get_user_model()


class SerializerMixin(object):

    def _get_user_object(self):
        request = self.context.get('request', None)
        user = None

        if request is not None:
            user = request.user

        return user

    def has_full_access(self):
        request = self.context.get('request', None)
        return (request is not None and
                (request.user.is_superuser or
                 request.user.role == User.ADMINISTRATOR))
