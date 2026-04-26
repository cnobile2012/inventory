#
# login/views.py
#

import json

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import auth
from django.template.context_processors import csrf

from inventory.apps.login.forms import LoginForm, RegistrationForm
from inventory.apps.utils.views import ViewBase
from inventory.settings import SITE_NAME, getLogger

log = getLogger()


class Login(ViewBase):
    """
    Called when the login page is requested.
    """
    def __init__(self, log, crumbData=()):
        super().__init__(log)
        self.__crumbData = crumbData

    def __call__(self, request, *args, **kwargs):
        # Set in session: kwargs.get('path')
        request.session.set_test_cookie()
        form = LoginForm()
        redirect = request.GET.get('/login/')
        context = {}
        username = request.user.username

        if isinstance(self.__crumbData, tuple) and len(self.__crumbData) == 2:
            title, img = self.__crumbData
            self._setBreadcrumb(request, title, '/login/')
            breadcrumbs = self._getBreadcrumbs(request)
            context['breadcrumb'] = {'pages': breadcrumbs, 'img': img}

        if username:
            tmpl = loader.get_template('login_user.html')
            context['user'] = username
        else:
            tmpl = loader.get_template('login_login.html')

        context['name'] = SITE_NAME
        context['form'] = form
        context['redirect'] = redirect
        self._log.debug("Context dump for %s: %s", self.__module__, context)
        response = HttpResponse(tmpl.render(context))
        response.set_cookie("csrftoken", request.META.get("CSRF_COOKIE", ""),
                            secure=True)
        return response


class Logout(ViewBase):
    """
    Called when the logout page is requested.
    """
    def __init__(self, log):
        super().__init__(log)

    def __call__(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect('/')


class ProcessLogin(ViewBase):
    """
    Called when the login page sends an AJAX request to validate a user.
    """
    def __init__(self, log):
        super().__init__(log)

    def __call__(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        context = {}
        user = auth.authenticate(username=username, password=password)
        self._log.info("User: %s, just logged in.", user)

        if user is not None:
            if user.is_active:
                # Test that the preset test cookie worked.
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                    # Set the user in the session.
                    auth.login(request, user)
                    context["valid"] = True
                    context["cookies"] = True
                    # context['logoutHTML'] = self._logoutHTML(user)
                    context["message"] = f"User [{username}] is logged in."
                else:
                    context["valid"] = True
                    context["cookies"] = False
                    context["message"] = ("Please enable cookies if you want "
                                          "to login")
            else:
                context["valid"] = False
                context["message"] = "The user [%s] is disabled."
        else:
            context["valid"] = False
            context["message"] = (f"Could not validate [{username}] as a "
                                  "user, check username and password.")
            username = username and username or None

        self._log.debug("Context dump for %s: %s", self.__module__, context)
        return HttpResponse(json.dumps(context))


class CreateUser(ViewBase):
    """
    Called when the createUser page is requested.
    """
    def __init__(self, log, crumbData=()):
        super().__init__(log)
        self.__crumbData = crumbData

    def __call__(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        form = RegistrationForm()
        context = {}
        username = request.user.username

        if isinstance(self.__crumbData, tuple):
            title, img = self.__crumbData
            self._setBreadcrumb(request, title, '/createUser/')
            breadcrumbs = self._getBreadcrumbs(request)
            context['breadcrumb'] = {'pages': breadcrumbs, 'img': img}

        if username:
            tmpl = loader.get_template('createUser_user.html')
            context['user'] = username
        else:
            tmpl = loader.get_template('createUser_login.html')

        context['name'] = SITE_NAME
        context['form'] = form
        context.update(csrf(request))
        self._log.debug("Context dump for %s: %s", self.__module__, context)
        return HttpResponse(tmpl.render(context))


class ProcessCreateUser(ViewBase):

    def __init__(self, log):
        super().__init__(log)

    def __call__(self, request, *args, **kwargs):
        context = {}
        form = RegistrationForm(request.POST)
        self._log.debug(request.POST)

        if form.is_valid():
            form.save()
            context['valid'] = True
            context['message'] = ("Your account is created. Please contact a "
                                  "sys admin to have your account upgraded.")
        else:
            context['valid'] = False
            context['content'] = self._formHTML(form, "create")

        self._log.debug("Context dump for %s: %s", self.__module__, context)
        return HttpResponse(json.dumps(context))


##############################
# Instantiate view callables #
##############################
# HTML calls
createUser = CreateUser(
    log, crumbData=("Create User", "/static/img/arrow18x16.png"))
login = Login(log, crumbData=("Login", "/static/img/arrow18x16.png"))
logout = Logout(log)

# AJAX calls
processLogin = ProcessLogin(log)
processCreateUser = ProcessCreateUser(log)
