#
# login/views.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2013-06-29 21:54:44 -0400 (Sat, 29 Jun 2013) $
# $Revision: 77 $
#----------------------------------

import simplejson
from StringIO import StringIO
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from django.contrib.auth.models import User
from django.contrib import auth
from django.db import models
from django.core.context_processors import csrf

from inventory.apps.login.forms import LoginForm, RegistrationForm
from inventory.apps.utils.views import ViewBase
from inventory.settings import SITE_NAME, getLogger


log = getLogger()


class Login(ViewBase):
    """
    Called when the login page is requested.
    """
    def __init__(self, log, crumbData=()):
        super(Login, self).__init__(log)
        self.__crumbData = crumbData

    def __call__(self, request, *args, **kwargs):
        # Set in session: kwargs.get('path')
        request.session.set_test_cookie()
        form = LoginForm()
        redirect = request.GET.get('/login/')
        response = {}
        username = request.user.username

        if isinstance(self.__crumbData, tuple) and len(self.__crumbData) == 2:
            title, img = self.__crumbData
            self._setBreadcrumb(request, title, '/login/')
            breadcrumbs = self._getBreadcrumbs(request)
            response['breadcrumb'] = {'pages': breadcrumbs, 'img': img}

        if username:
            tmpl = loader.get_template('login_user.html')
            response['user'] = username
        else:
            tmpl = loader.get_template('login_login.html')

        response['name'] = SITE_NAME
        response['form'] = form
        response['redirect'] = redirect
        context = Context(response)
        context.update(csrf(request))
        self._log.debug("Context dump for %s: %s", self.__module__, context)
        return HttpResponse(tmpl.render(context))


class Logout(ViewBase):
    """
    Called when the logout page is requested.
    """
    def __init__(self, log):
        super(Logout, self).__init__(log)

    def __call__(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect('/')


class ProcessLogin(ViewBase):
    """
    Called when the login page sends an AJAX request to validate a user.
    """
    def __init__(self, log):
        super(ProcessLogin, self).__init__(log)

    def __call__(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        response = {}
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                # Test that the preset test cookie worked.
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                    # Set the user in the session.
                    auth.login(request, user)
                    response["valid"] = True
                    response["cookies"] = True
                    #response['logoutHTML'] = self._logoutHTML(user)
                    response["message"] = u"User [%s] is logged in." % username
                else:
                    response["valid"] = True
                    response["cookies"] = False
                    response["message"] = u"Please enable cookies if you" + \
                                          u" want to login"
            else:
                response["valid"] = False
                response["message"] = u"The user [%s] is disabled."
        else:
            response["valid"] = False
            response["message"] = u"Could not validate [%s] as a user," + \
                                  u" check username and password."
            username = username and username or None
            response["message"] =  response["message"] % username

        self._log.debug("Context dump for %s: %s", self.__module__, response)
        return HttpResponse(simplejson.dumps(response))

##     def _logoutHTML(self, user):
##         result = u'''
##         <li class="user">User: %s</li>
##         <li class="user"><a href="/login/logout/">Logout</a></li>
## ''' % user.username
##         return result


class CreateUser(ViewBase):
    """
    Called when the createUser page is requested.
    """
    def __init__(self, log, crumbData=()):
        super(CreateUser, self).__init__(log)
        self.__crumbData = crumbData

    def __call__(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        form = RegistrationForm()
        response = {}
        username = request.user.username

        if isinstance(self.__crumbData, tuple):
            title, img = self.__crumbData
            self._setBreadcrumb(request, title, '/createUser/')
            breadcrumbs = self._getBreadcrumbs(request)
            response['breadcrumb'] = {'pages': breadcrumbs, 'img': img}

        if username:
            tmpl = loader.get_template('createUser_user.html')
            response['user'] = username
        else:
            tmpl = loader.get_template('createUser_login.html')

        response['name'] = SITE_NAME
        response['form'] = form
        context = Context(response)
        context.update(csrf(request))
        self._log.debug("Context dump for %s: %s", self.__module__, context)
        return HttpResponse(tmpl.render(context))


class ProcessCreateUser(ViewBase):

    def __init__(self, log):
        super(ProcessCreateUser, self).__init__(log)

    def __call__(self, request, *args, **kwargs):
        response = {}
        form = RegistrationForm(request.POST)
        self._log.debug(request.POST)

        if form.is_valid():
            newUser = form.save()
            response['valid'] = True
            response['message'] = u"Your account is created. Please " + \
                                  u"contact a sys admin to have your " + \
                                  u"account upgraded."
        else:
            response['valid'] = False
            response['content'] = self._formHTML(form, "create")

        self._log.debug(u"Context dump for %s: %s", self.__module__, response)
        return HttpResponse(simplejson.dumps(response))


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
