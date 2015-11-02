# -*- coding: utf-8 -*-
#
# inventory/oauth2/api/views.py
#

import logging

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from rest_condition import ConditionalPermission, C, And, Or, Not

from oauth2_provider.models import (
    Grant, AccessToken, RefreshToken, get_application_model)
from oauth2_provider.ext.rest_framework import (
    TokenHasReadWriteScope, TokenHasScope)

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectManager, IsAnyUser)
from inventory.common.api.pagination import SmallResultsSetPagination

from .serializers import (
    ApplicationSerializer, AccessTokenSerializer, RefreshTokenSerializer,
    GrantSerializer)


log = logging.getLogger('api.oauth2.views')
Application = get_application_model()


#
# Application
#
class ApplicationAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if self.request.user.is_superuser:
            result = Application.objects.all()
        else:
            result = self.request.user.oauth2_provider_application.all()

        return result


class ApplicationList(ApplicationAuthorizationMixin, ListCreateAPIView):
    """
    Oauth2 Application list endpoint.

    ## Valid Values:
      1. `client_type`
        * `confidential`
        * `public`
      2. `authorization_grant_type`
        * `authorization-code`
        * `implicit`
        * `password`
        * `client-credentials`
      3. `redirect_uris`
        * URIs can be seperated with any whitespace character.
    """
    serializer_class = ApplicationSerializer
    permission_classes = (
        And(
            Or(IsAnyUser),
            Or(TokenHasScope, IsAuthenticated)
            ),
        )
    required_scopes = ('read', 'write',)
    pagination_class = SmallResultsSetPagination

application_list = ApplicationList.as_view()


class ApplicationDetail(ApplicationAuthorizationMixin,
                        RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = (
        And(
            Or(IsAnyUser),
            Or(TokenHasScope, IsAuthenticated)
            ),
        )
    required_scopes = ('read', 'write',)

application_detail = ApplicationDetail.as_view()


#
# AccessToken
#
class AccessTokenAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if self.request.user.is_superuser:
            result = AccessToken.objects.all()
        else:
            for app in self.request.user.oauth2_provider_application.all():
                for token in app.accesstoken_set.all():
                    result.append(token)

        return result


class AccessTokenList(AccessTokenAuthorizationMixin, ListCreateAPIView):
    """
    Oauth2 AccessToken list endpoint.
    """
    serializer_class = AccessTokenSerializer
    permission_classes = (
        And(
            Or(IsAnyUser),
            Or(TokenHasScope, IsAuthenticated)
            ),
        )
    required_scopes = ('read', 'write',)
    pagination_class = SmallResultsSetPagination

access_token_list = AccessTokenList.as_view()


class AccessTokenDetail(AccessTokenAuthorizationMixin,
                        RetrieveUpdateDestroyAPIView):
    serializer_class = AccessTokenSerializer
    permission_classes = (
        And(
            Or(IsAnyUser),
            Or(TokenHasScope, IsAuthenticated)
            ),
        )
    required_scopes = ('read', 'write',)

access_token_detail = AccessTokenDetail.as_view()


#
# Grant
#
class GrantAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if self.request.user.is_superuser:
            result = Grant.objects.all()
        else:
            for app in self.request.user.oauth2_provider_application.all():
                for grant in app.grant_set.all():
                    result.append(grant)

        return result


class GrantList(GrantAuthorizationMixin, ListCreateAPIView):
    """
    Oauth2 Grant list endpoint.
    """
    serializer_class = GrantSerializer
    permission_classes = (
        And(
            Or(IsAnyUser),
            Or(TokenHasScope, IsAuthenticated)
            ),
        )
    required_scopes = ('read', 'write',)
    pagination_class = SmallResultsSetPagination

grant_list = GrantList.as_view()


class GrantDetail(GrantAuthorizationMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = GrantSerializer
    permission_classes = (
        And(
            Or(IsAnyUser),
            Or(TokenHasScope, IsAuthenticated)
            ),
        )
    required_scopes = ('read', 'write',)

grant_detail = GrantDetail.as_view()


#
# RefreshToken
#
class RefreshTokenAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if self.request.user.is_superuser:
            result = RefreshToken.objects.all()
        else:
            for app in self.request.user.oauth2_provider_application.all():
                for token in app.refreshtoken_set.all():
                    result.append(token)

        return result


class RefreshTokenList(RefreshTokenAuthorizationMixin, ListCreateAPIView):
    """
    Oauth2 RefreshToken list endpoint.
    """
    serializer_class = RefreshTokenSerializer
    permission_classes = (
        And(
            Or(IsAnyUser),
            Or(TokenHasScope, IsAuthenticated)
            ),
        )
    required_scopes = ('read', 'write',)
    pagination_class = SmallResultsSetPagination

refresh_token_list = RefreshTokenList.as_view()


class RefreshTokenDetail(RefreshTokenAuthorizationMixin,
                         RetrieveUpdateDestroyAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (
        And(
            Or(IsAnyUser),
            Or(TokenHasScope, IsAuthenticated)
            ),
        )
    required_scopes = ('read', 'write',)

refresh_token_detail = RefreshTokenDetail.as_view()
