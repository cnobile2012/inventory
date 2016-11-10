# -*- coding: utf-8 -*-
#
# inventory/accounts/api/views.py
#

import logging

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView)
from rest_framework.permissions import IsAuthenticated

from rest_condition import ConditionalPermission, C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsDefaultUser, IsAnyUser, IsReadOnly,
    IsProjectOwner, IsProjectManager, IsProjectDefaultUser, IsAnyProjectUser,
    IsUserActive, IsPostOnly)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.common.api.view_mixins import (
    TrapDjangoValidationErrorCreateMixin, TrapDjangoValidationErrorUpdateMixin)

from ..models import Question, Answer
from .serializers import (
    UserSerializer, QuestionSerializer, AnswerSerializer)

log = logging.getLogger('api.accounts.views')
UserModel = get_user_model()


#
# User
#
class UserAuthorizationMixin(object):

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = UserModel.objects.all()
        else:
            result = UserModel.objects.filter(pk=self.request.user.pk)

        return result


class UserList(TrapDjangoValidationErrorCreateMixin,
               UserAuthorizationMixin,
               ListCreateAPIView):
    """
    User list endpoint.
    """
    serializer_class = UserSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
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
    lookup_field = 'public_id'

user_list = UserList.as_view()


class UserDetail(TrapDjangoValidationErrorUpdateMixin,
                 UserAuthorizationMixin,
                 RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAnyUser,
               IsAnyProjectUser
               )
            ),
        )
    lookup_field = 'public_id'

user_detail = UserDetail.as_view()


#
# Group
#
## class GroupAuthorizationMixin(object):

##     def get_queryset(self):
##         if (self.request.user.is_superuser or
##             self.request.user.role == UserModel.ADMINISTRATOR):
##             result = Group.objects.all()
##         else:
##             result = self.request.user.groups.all()

##         return result


## class GroupList(TrapDjangoValidationErrorCreateMixin,
##                 GroupAuthorizationMixin,
##                 ListCreateAPIView):
##     """
##     Group list endpoint.
##     """
##     serializer_class = GroupSerializer
##     permission_classes = (
##         And(IsUserActive, #IsAuthenticated,
##             Or(IsAdminSuperUser,
##                IsAdministrator)
##             ),
##         )
##     required_scopes = ('read', 'write', 'groups',)
##     pagination_class = SmallResultsSetPagination

## group_list = GroupList.as_view()


## class GroupDetail(TrapDjangoValidationErrorUpdateMixin,
##                   GroupAuthorizationMixin,
##                   RetrieveUpdateAPIView):
##     serializer_class = GroupSerializer
##     permission_classes = (
##         And(IsUserActive, #IsAuthenticated,
##             Or(IsAdminSuperUser,
##                IsAdministrator)
##             ),
##         )
##     required_scopes = ('read', 'write', 'groups',)

## group_detail = GroupDetail.as_view()


#
# Question
#
class QuestionList(TrapDjangoValidationErrorCreateMixin,
                   ListCreateAPIView):
    """
    Question list endpoint.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
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
                     RetrieveUpdateAPIView):
    """
    Question detail endpoint.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (
         And(IsUserActive, #IsAuthenticated,
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
class AnswerAuthorizationMixin(object):

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = Answer.objects.all()
        else:
            result = self.request.user.answers.all()

        return result


class AnswerList(TrapDjangoValidationErrorCreateMixin,
                 AnswerAuthorizationMixin,
                 ListCreateAPIView):
    """
    Answer list endpoint.
    """
    serializer_class = AnswerSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAnyUser,
               IsAnyProjectUser)
            ),
        )
    pagination_class = SmallResultsSetPagination
    lookup_field = 'public_id'

answer_list = AnswerList.as_view()


class AnswerDetail(TrapDjangoValidationErrorUpdateMixin,
                   AnswerAuthorizationMixin,
                   RetrieveUpdateDestroyAPIView):
    """
    Answer detail endpoint.
    """
    serializer_class = AnswerSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAnyUser,
               IsAnyProjectUser)
            ),
        )
    lookup_field = 'public_id'

answer_detail = AnswerDetail.as_view()
