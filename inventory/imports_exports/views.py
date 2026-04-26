#
# moscot/exports_imports/views.py
#

import logging
import os

from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required
from django.utils.http import urlquote
#from django.utils.translation import gettext_lazy as _

from moscot.settings import TMP_IMPORT_PATH
from moscot.tracking.models import Tracking
from moscot.scope_requests.models import ScopeRequest
from moscot.common.view_mixins import JSONResponseMixin

from .models import DataImportFormat
from .forms import UploadFileForm, DataVerifyForm
from .tracking_first_pass import CSVFirstPassValidation
from .tracking_second_pass import CSVSecondPassSubmit

log = logging.getLogger('moscot.views')


#
# UploadFile
#
class UploadFileView(FormView):
    template_name = 'exports_imports/upload_file_view.html'
    form_class = UploadFileForm

    def form_valid(self, form):
        u_file = form.cleaned_data.get(u'u_file')
        self.f_type = form.cleaned_data.get(u'f_type')
        self.model_name = form.cleaned_data.get(u'model')
        log.debug("u_file: %s, f_type: %s, model: %s",
                  u_file , self.f_type, self.model_name)

        if u_file:
            self.filename = u_file.name
            path = os.path.join(TMP_IMPORT_PATH, self.filename)

            with open(path, u'wb') as f:
                for chunk in u_file.chunks():
                    f.write(chunk)

            log.info("Wrote '%s'", path)
        else:
            log.error("Invalid file name: %s", u_file)

        return super(UploadFileView, self).form_valid(form)

    def get_success_url(self):
        url = reverse('upload-verify', args=(self.model_name, self.f_type,
                                             urlquote(self.filename)))
        log.debug("url: %s", url)
        return url

upload_file_view = UploadFileView.as_view()


#
# DataVerifyView
#
class DataFormatChoiceView(FormView):
    template_name = 'exports_imports/data_verify_view.html'
    form_class = DataVerifyForm
    _MODEL_NAME_MAP = {
        Tracking.__name__.lower(): Tracking._meta.verbose_name,
        ScopeRequest.__name__.lower(): ScopeRequest._meta.verbose_name,
        }

    def dispatch(self, request, *args, **kwargs):
        log.debug("args: %s, kwargs: %s", args, kwargs)
        self.user = request.user
        self.model_name = kwargs.get(u'model')
        self.f_type = kwargs.get(u'f_type')
        self.filename = kwargs.get(u'filename')
        return super(DataFormatChoiceView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DataFormatChoiceView, self).get_context_data(**kwargs)
        context[u'title'] = self._MODEL_NAME_MAP.get(self.model_name)
        context[u'model_name'] = self.model_name
        context[u'f_type'] = self.f_type
        context[u'filename'] = self.filename
        context[u'formats'] = (DataImportFormat.objects.
                               get_user_global_formats(self.user))
        return context

    def get_initial(self):
        return {
            u'model_name': self.model_name,
            }

data_format_choice_view = DataFormatChoiceView.as_view()


#
# DataValidateAJAXView
#
class DataValidateAJAXView(JSONResponseMixin, View):
    http_method_names = ('post',)

    def get_context_data(self, **kwargs):
        context = {'valid': True, 'errors': False}
        pk = kwargs.pop(u'pk', None)
        f_type = kwargs.pop(u'f_type', None)
        model_name = kwargs.pop(u'model_name', None)
        obj = None

        try:
            obj = DataImportFormat.objects.get(pk=pk)

            if obj.model != model_name:
                msg = u"Invalid {} model, found {}".format(
                    DataImportFormat.MODELS_MAP.get(model_name), model_name)
                log.error(msg)
                context[u'valid'] = False
                context[u'message'] = msg
                obj = None
        except DataImportFormat.DoesNotExist as e:
            msg = "Invalid DataImportFormat pk: {}, {}".format(pk, e)
            log.error(msg)
            context[u'valid'] = False
            context[u'message'] = msg

        if obj:
            kwargs['formatObj'] = obj
            # TO DO test for f_type when we can import file types other
            # than the CSV file type. Form now drop f_type on the floor.
            fpv = CSVFirstPassValidation(log, **kwargs)
            pd_idx = 1
            rows = []
            data = []

            try:
                rows[:], fields_size, row_size = fpv.validate()
            except (IOError, IndexError) as e:
                context[u'message'] = str(e)
                context[u'valid'] = False
            else:
                for row_idx, row in enumerate(rows):
                    if row_idx == 0:
                        pd_idx = row.index(u'project-details')
                        continue

                    if row[0].lower() == u'fail':
                        data.append((row_idx, row[pd_idx]))

                data_size = len(data)
                size_diff = cmp(fields_size, row_size)

                if cmp(fields_size, row_size) == -1:
                    extra_msg = (
                        u" The chosen format is expecting {0} columns, your "
                        u"file has {1} columns anything after {0} will be "
                        u"truncated if you choose to submit. "
                        ).format(fields_size, row_size)
                else:
                    extra_msg = u''

                if data_size > 0:
                    context[u'message'] = (
                        u"View the errors in your file below. The first field "
                        u"is the row number in your file (not including the "
                        u"header) that contains the error. The second field "
                        u"is the 'Project Detail' column indicating the "
                        u"columns that have errors plus any project details "
                        u"you may have in the row.") + extra_msg
                    context[u'errors'] = True
                else:
                    context[u'message'] = extra_msg + (
                        u"Found no failures in your file. You may click the "
                        u"Submit button below to create/update {} records."
                        ).format(row_idx)
                    context[u'errors'] = False

                context[u'data'] = data
                context[u'fail_count'] = data_size
                context[u'total_count'] = len(rows) - 1

        return context

    def post(self, request, *args, **kwargs):
        log.debug("request: %s, args: %s, kwargs: %s", request, args, kwargs)
        kwargs[u'fullpath'] = os.path.join(TMP_IMPORT_PATH,
                                           request.POST.get(u'filename'))
        kwargs[u'f_type'] = request.POST.get(u'fType')
        kwargs[u'model_name'] = request.POST.get(u'modelName')
        kwargs[u'pk'] = request.POST.get(u'pk')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

data_validate_ajax_view = DataValidateAJAXView.as_view()


#
# DataSubmitAJAXView
#
class DataSubmitAJAXView(JSONResponseMixin, View):
    http_method_names = ('post',)

    def get_context_data(self, **kwargs):
        log.debug("kwargs: %s", kwargs)
        context = {u'valid': True}
        pk = kwargs.pop(u'pk', None)
        f_type = kwargs.pop(u'f_type', None) # Not used at this time.
        model_name = kwargs.pop(u'model_name', None)
        user = kwargs.pop(u'user', None)
        obj = None

        try:
            obj = DataImportFormat.objects.get(pk=pk)

            if obj.model != model_name:
                msg = u"Invalid {} model, found {}".format(
                    DataImportFormat.MODELS_MAP.get(model_name), model_name)
                log.error(msg)
                context[u'valid'] = False
                context[u'message'] = msg
                obj = None
        except DataImportFormat.DoesNotExist as e:
            msg = "Invalid DataImportFormat pk: {}, {}".format(pk, e)
            log.error(msg)
            context[u'valid'] = False
            context[u'message'] = msg

        if obj:
            kwargs[u'formatObj'] = obj
            sps = CSVSecondPassSubmit(log, user, **kwargs)

            try:
                sps.submit()
            except (IOError, IndexError) as e:
                context[u'valid'] = False
                context[u'message'] = str(e)
            else:
                context[u'message'] = (u"Your data has been saved to the "
                                       u"database.")

        return context

    def post(self, request, *args, **kwargs):
        log.debug("request: %s, args: %s, kwargs: %s", request, args, kwargs)
        kwargs[u'user'] = request.user
        kwargs[u'fullpath'] = os.path.join(TMP_IMPORT_PATH,
                                           request.POST.get(u'filename'))
        kwargs[u'model_name'] = request.POST.get(u'modelName')
        kwargs[u'pk'] = request.POST.get(u'pk')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

data_submit_ajax_view = DataSubmitAJAXView.as_view()
