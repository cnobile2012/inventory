#
# inventory/accounts/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from inventory.common.admin_mixins import UserAdminMixin

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


#
# User
#
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'send_email',
                           'need_password',)}),
        (_("Personal Info"), {'fields': ('picture', 'first_name', 'last_name',
                                         'address_01', 'address_02', 'city',
                                         'region', 'postal_code', 'country',
                                         'dob', 'email', 'answers',)}),
        (_("Projects"), {'fields': ('role', 'projects',)}),
        (_("Permissions"), {'classes': ('collapse',),
                            'fields': ('is_active', 'is_staff',
                                       'is_superuser', 'groups',
                                       'user_permissions',)}),
        (_("Status"), {'classes': ('collapse',),
                       'fields': ('last_login', 'date_joined',)}),
        )
    readonly_fields = ('last_login', 'date_joined',)
    list_display = ('_image_thumb_producer', 'username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_active',
                    '_image_url_producer',)
    list_editable = ('is_staff', 'is_active',)
    search_fields = ('username', 'last_name', 'email',)
    filter_horizontal = ('projects', 'groups', 'user_permissions', 'answers',)

    class Media:
        js = ('js/js.cookie-2.0.4.min.js',
              'js/inheritance.js',
              'js/regions.js',)


#
# Question
#
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
class AnswerAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('question', 'answer',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('creator', 'created', 'updater', 'updated',)
    list_display = ('question', '_owner_producer', 'answer', 'updater',
                    'updated',)
    form = AnswerForm


admin.site.register(get_user_model(), UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
