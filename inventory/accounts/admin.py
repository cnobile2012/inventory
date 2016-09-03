# -*- coding: utf-8 -*-
#
# inventory/accounts/admin.py
#
"""
Accounts admin.
"""
__docformat__ = "restructuredtext en"

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

from inventory.common.admin_mixins import UserAdminMixin

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


#
# User
#
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('public_id', 'username', 'password',)}),
        (_("Personal Info"), {'fields': ('picture', 'first_name', 'last_name',
                                         'address_01', 'address_02', 'city',
                                         'subdivision', 'postal_code',
                                         'country', 'dob', 'email', 'language',
                                         'timezone', 'answers',)}),
        (_("Projects"), {'fields': ('_role', 'project_default',)}),
        (_("Permissions"), {'classes': ('collapse',),
                            'fields': ('is_active', 'is_staff',
                                       'is_superuser', 'groups',
                                       'user_permissions',)}),
        (_("Status"), {'classes': ('collapse',),
                       'fields': ('send_email', 'need_password', 'last_login',
                                  'date_joined',)}),
        )
    readonly_fields = ('public_id', 'last_login', 'date_joined',)
    list_display = ('image_thumb_producer', 'public_id', 'username', 'email',
                    'first_name', 'last_name', 'is_staff', 'is_active',
                    'image_url_producer',)
    list_editable = ('is_staff', 'is_active',)
    search_fields = ('username', 'last_name', 'email', 'public_id',)
    filter_horizontal = ('groups', 'user_permissions', 'answers',)

    class Media:
        js = ('js/js.cookie-2.0.4.min.js',
              'js/inheritance.js',
              'js/regions.js',)

admin.site.register(get_user_model(), UserAdmin)


#
# Question
#
@admin.register(Question)
class QuestionAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('question',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('active', 'creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('creator', 'created', 'updater', 'updated',)
    list_display = ('question', 'active', 'updater', 'updated',)
    list_editable = ('active',)
    list_filter = ('active',)
    form = QuestionForm


#
# Answer
#
@admin.register(Answer)
class AnswerAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('question', 'answer',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('creator', 'created', 'updater', 'updated',)
    list_display = ('question', 'user_producer', 'answer', 'updater',
                    'updated',)
    form = AnswerForm
