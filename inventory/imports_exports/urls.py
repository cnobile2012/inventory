#
# inventory/imports_exports/urls.py
#

from django.urls import re_path


urlpatterns = [
    re_path(r'upload-file/$', 'upload_file_view',
            name="upload-file"),
    re_path(r'upload-verify/(?P<model>.+)/(?P<f_type>.+)/(?P<filename>.+)/$',
            'data_format_choice_view', name="upload-verify"),
    re_path(r'upload-validate/$', 'data_validate_ajax_view',
            name="upload-validate"),
    re_path(r'upload-submit/$', 'data_submit_ajax_view',
            name="upload-submit"),
    ]
