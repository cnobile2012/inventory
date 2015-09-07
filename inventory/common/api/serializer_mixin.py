#
# inventory/common/api/serializer_mixin.py
#


class SerializerMixin(object):

    def _get_user_object(self):
        request = self.context.get('request', None)
        user = None

        if request:
            user = request.user

        return user
