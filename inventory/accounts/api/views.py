# -*- coding: utf-8 -*-
#
# inventory/accounts/api/views.py
#
"""
Account API Views
"""
__docformat__ = "restructuredtext en"

import base64
import logging
import re
import string
from decimal import Decimal

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model, login, logout
from django.utils.translation import gettext_lazy as _

from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView,
    GenericAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings
from rest_framework.status import (
    HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_401_UNAUTHORIZED)
from rest_framework.views import APIView

from rest_condition import C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsDefaultUser, IsAnyUser, IsReadOnly,
    IsProjectOwner, IsProjectManager, IsProjectDefaultUser, IsAnyProjectUser,
    IsUserActive, IsPostOnly)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.common.api.parsers import parser_factory
from inventory.common.api.renderers import renderer_factory
from inventory.common.api.view_mixins import (
    TrapDjangoValidationErrorCreateMixin, TrapDjangoValidationErrorUpdateMixin)

from ..models import Question, Answer
from .serializers import (
    UserSerializerVer01, PublicUserSerializerVer01, QuestionSerializerVer01,
    AnswerSerializerVer01, LoginSerializerVer01)

log = logging.getLogger('api.accounts.views')
UserModel = get_user_model()


#
# User
#
class UserMixin:
    parser_classes = (parser_factory('users')
                      + api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (renderer_factory('users')
                        + api_settings.DEFAULT_RENDERER_CLASSES)
    ADMINISTRATOR = UserModel.ROLE_MAP[UserModel.ADMINISTRATOR]

    def get_serializer_class(self):
        serializer = None

        if (self.request.user.is_superuser
            or self.request.user.role == self.ADMINISTRATOR
            or (self.kwargs and self.request.user == self.get_object())):

            if self.request.version == Decimal("1"):
                serializer = UserSerializerVer01
                # elif self.request.version == Decimal("2"):
                #    serializer = UserSerializerVer02
        else:
            if self.request.version == Decimal("1"):
                serializer = PublicUserSerializerVer01
                # elif self.request.version == Decimal("2"):
                #    serializer = PublicUserSerializerVer02

        return serializer

    def get_queryset(self):
        return UserModel.objects.all()


class UserList(TrapDjangoValidationErrorCreateMixin,
               UserMixin,
               ListCreateAPIView):
    """
    User list endpoint.
    """
    permission_classes = (
        And(IsUserActive,
            IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               And(IsReadOnly,
                   Or(IsDefaultUser,
                      IsAnyProjectUser)
                   )
               )
            ),
        )
    pagination_class = SmallResultsSetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'first_name', 'last_name', 'email',)
    lookup_field = 'public_id'

user_list = UserList.as_view()


class UserDetail(TrapDjangoValidationErrorUpdateMixin,
                 UserMixin,
                 RetrieveUpdateAPIView):
    permission_classes = (
        And(IsUserActive,
            IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               Or(IsAnyUser,
                  IsAnyProjectUser
                  )
               )
            ),
        )
    lookup_field = 'public_id'

user_detail = UserDetail.as_view()


#
# Group
#
## class GroupMixin:
##     ADMINISTRATOR = UserModel.ROLE_MAP[UserModel.ADMINISTRATOR]

##     def get_serializer_class(self):
##         serializer = None

##         if self.request.version == Decimal("1"):
##             serializer = GroupSerializerVer01
##         # elif self.request.version == Decimal("2"):
##         #    serializer = GroupSerializerVer02

##         return serializer

##     def get_queryset(self):
##         if (self.request.user.is_superuser or
##             self.request.user.role == self.ADMINISTRATOR):
##             result = Group.objects.all()
##         else:
##             result = self.request.user.groups.all()

##         return result


## class GroupList(TrapDjangoValidationErrorCreateMixin,
##                 GroupMixin,
##                 ListCreateAPIView):
##     """
##     Group list endpoint.
##     """
##     permission_classes = (
##         And(IsUserActive, IsAuthenticated,
##             Or(IsAdminSuperUser,
##                IsAdministrator)
##             ),
##         )
##     required_scopes = ('read', 'write', 'groups',)
##     pagination_class = SmallResultsSetPagination

## group_list = GroupList.as_view()


## class GroupDetail(TrapDjangoValidationErrorUpdateMixin,
##                   GroupMixin,
##                   RetrieveUpdateAPIView):
##     permission_classes = (
##         And(IsUserActive, IsAuthenticated,
##             Or(IsAdminSuperUser,
##                IsAdministrator)
##             ),
##         )
##     required_scopes = ('read', 'write', 'groups',)

## group_detail = GroupDetail.as_view()


#
# Question
#
class QuestionMixin:
    parser_classes = (parser_factory('questions')
                      + api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (renderer_factory('questions')
                        + api_settings.DEFAULT_RENDERER_CLASSES)

    def get_serializer_class(self):
        serializer = None

        if self.request.version == Decimal("1"):
            serializer = QuestionSerializerVer01
        # elif self.request.version == Decimal("2"):
        #    serializer = QuestionSerializerVer02

        return serializer


class QuestionList(TrapDjangoValidationErrorCreateMixin,
                   QuestionMixin,
                   ListCreateAPIView):
    """
    Question list endpoint.
    """
    queryset = Question.objects.all()
    permission_classes = (
        And(IsUserActive,
            IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               And(IsReadOnly, Or(IsDefaultUser,
                                  IsAnyProjectUser)
                   )
               )
            ),
        )
    pagination_class = SmallResultsSetPagination
    lookup_field = 'public_id'

question_list = QuestionList.as_view()


class QuestionDetail(TrapDjangoValidationErrorUpdateMixin,
                     QuestionMixin,
                     RetrieveUpdateAPIView):
    """
    Question detail endpoint.
    """
    queryset = Question.objects.all()
    permission_classes = (
         And(IsUserActive,
             IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               And(IsReadOnly, Or(IsDefaultUser,
                                  IsAnyProjectUser)
                   )
               )
            ),
        )
    lookup_field = 'public_id'

question_detail = QuestionDetail.as_view()


#
# Answer
#
class AnswerMixin:
    parser_classes = (parser_factory('answers')
                      + api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (renderer_factory('answers')
                        + api_settings.DEFAULT_RENDERER_CLASSES)
    ADMINISTRATOR = UserModel.ROLE_MAP[UserModel.ADMINISTRATOR]

    def get_serializer_class(self):
        serializer = None

        if self.request.version == Decimal("1"):
            serializer = AnswerSerializerVer01
        # elif self.request.version == Decimal("2"):
        #    serializer = AnswerSerializerVer02

        return serializer

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == self.ADMINISTRATOR):
            result = Answer.objects.all()
        else:
            result = self.request.user.answers.all()

        return result


class AnswerList(TrapDjangoValidationErrorCreateMixin,
                 AnswerMixin,
                 ListCreateAPIView):
    """
    Answer list endpoint.
    """
    permission_classes = (
        And(IsUserActive,
            IsAuthenticated,
            Or(IsAnyUser,
               IsAnyProjectUser)
            ),
        )
    pagination_class = SmallResultsSetPagination
    lookup_field = 'public_id'

answer_list = AnswerList.as_view()


class AnswerDetail(TrapDjangoValidationErrorUpdateMixin,
                   AnswerMixin,
                   RetrieveUpdateDestroyAPIView):
    """
    Answer detail endpoint.
    """
    permission_classes = (
        And(IsUserActive,
            IsAuthenticated,
            Or(IsAnyUser,
               IsAnyProjectUser)
            ),
        )
    lookup_field = 'public_id'

answer_detail = AnswerDetail.as_view()


#
# Login
#
class LoginView(GenericAPIView):
    """
    Login view. Performs a login on a POST and provides the user's full
    name and the href to the user's endpoint. Credentials are required to
    login.
    """
    parser_classes = (parser_factory('login')
                      + api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (renderer_factory('login')
                        + api_settings.DEFAULT_RENDERER_CLASSES)
    serializer_class = LoginSerializerVer01
    permission_classes = ()
    CHARS = string.ascii_letters + string.digits + '+/='
    # The regex below will ignore any additional parameters as per RFC7617.
    RE_SEARCH = re.compile(
        r"^.*(Basic +)(?P<enc_creds>[{}]+) *.*$".format(CHARS))

    def post(self, request, *args, **kwargs):
        basic = request.META.get('HTTP_AUTHORIZATION')
        sre = self.RE_SEARCH.search('' if basic is None else basic)
        enc_creds = sre.group('enc_creds') if sre is not None else ""
        data = {}

        # Parse out the username and password.
        if len(enc_creds) > 0:
            creds = base64.b64decode(bytearray(enc_creds, 'utf-8')).decode()
            username, delm, password = creds.partition(':')
            data['username'] = username
            data['password'] = password

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        login(request, user)
        result = {}
        result['fullname'] = user.get_full_name_or_username()
        result['href'] = reverse(
            'user-detail', kwargs={'public_id': user.public_id},
            request=request)
        return Response(result)

login_view = LoginView.as_view()


#
# Logout
#
class LogoutView(APIView):
    """
    Logout view. Performs the logout on a POST. No POST data is required
    to logout.
    """
    parser_classes = (parser_factory('logout')
                      + api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (renderer_factory('logout')
                        + api_settings.DEFAULT_RENDERER_CLASSES)
    permission_classes = (
        And(IsUserActive,
            IsAuthenticated,
            Or(IsAnyUser,
               IsAnyProjectUser)
            ),
        )

    def post(self, request, *args, **kwargs):
        logout(request)
        status = HTTP_200_OK
        result = {'detail': _("Logout was successful.")}
        return Response(result, status=status)

logout_view = LogoutView.as_view()
