#
# utils/views.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2010-08-31 15:14:49 -0400 (Tue, 31 Aug 2010) $
# $Revision: 14 $
#----------------------------------

class ViewBase(object):
    __CRUMBS_KEY = 'breadcrumbs'

    def __init__(self, log):
        self._log = log

    ## @classmethod
    ## def getLocalizedNowDateTime(self):
    ##     timezone = pytz.timezone(TIME_ZONE)
    ##     return datetime.datetime.now(timezone)

    ## def getUserFromSession(self, key):
    ##     #key = request.session.session_key
    ##     session = Session.objects.get(session_key=key)
    ##     uid = session.get_decoded().get('_auth_user_id')
    ##     return User.objects.get(pk=uid)

    def _formHTML(self, form, klass=None):
        result = u'''
          <form id="form" method="post" action="javascript:void(0)">
            <ul class="%s">
              %s
            </ul>
            <div class="submit">
              <input id="submit" type="submit" value="Submit" />
            </div> <!-- End div.submit -->
          </form>
        ''' % (klass, form.as_ul().replace('\n', '\n              '))
        return result

    ## def _buildResponse(self, status, message):
    ##     # RFC-2616 states that: "All 1xx (informational), 204 (no content),
    ##     # and 304 (not modified) responses MUST NOT include a message-body".
    ##     if status in (100, 101, 102, 204, 304): return ''
    ##     response = {}
    ##     response['title'] = "%s %s" % (status, STATUS_CODES.get(
    ##         status, 'Invalid Status'))
    ##     response['message'] = str(message)
    ##     context = Context(response)
    ##     self._log.debug("Context dump for %s: %s", self.__module__, context)
    ##     tmpl = loader.get_template('response.html')
    ##     return tmpl.render(context)

    def _setBreadcrumb(self, request, title, url):
        page = (title, url)
        self._log.debug("Current page: %s", page)

        try:
            breadcrumbs = request.session[self.__CRUMBS_KEY]
        except:
            breadcrumbs = []
            request.session[self.__CRUMBS_KEY] = breadcrumbs
            self._log.debug("Created %s object in session", self.__CRUMBS_KEY)

        if page in breadcrumbs:
            idx = breadcrumbs.index(page)
            self._log.debug("Deleting pages: %s", breadcrumbs[idx + 1:])
            del breadcrumbs[idx + 1:]
            # Must copy the 'breadcrumb' list back into the session, because
            # 'del' seems to create a new object for 'breadcrumbs'.
            request.session[self.__CRUMBS_KEY] = breadcrumbs
        else:
            breadcrumbs.append(page)
            self._log.debug("Saved %s to %s in session.",
                            page, self.__CRUMBS_KEY)

    def _getBreadcrumbs(self, request):
        result = request.session.get(self.__CRUMBS_KEY, [])
        self._log.debug("Breadcrumbs returned: %s", result)
        return result
