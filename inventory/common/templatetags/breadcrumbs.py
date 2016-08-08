#
# breadcrumbs.py
#
# Breadcrumbs tag library.
#
# SVN/CVS keywords
#------------------------------
# $Author: cnobile $
# $Date: 2013-06-29 21:55:28 -0400 (Sat, 29 Jun 2013) $
# $Revision: 78 $
#------------------------------

import logging

from django.utils import six
from django import template

log = logging.getLogger('inventory.common.templatetags')

register = template.Library()

@register.tag
def breadcrumbs(parser, token):
    """
    Renders the breadcrumbs. The tag can be used in two different ways either
    passing in a context or literal arguments in the HTML.

    Arguments:

     1. pages -- A list of tuples. ex. [('Home', '/'), ('Current Page', ''), ...]
     2. img   -- (optional) An image to display as the breadcrumb separator.
        If not passed to the tag the &raquo; entity will be used as a separator.

    Examples:

     * {% breadcrumbs "[('Home', 'url01'), ('Page01', 'url02'), ('CurrentPage', '/')]" %}
     * {% breadcrumbs page_context_var '/static/img/arrow18x16.png' %}
     * {% breadcrumbs page_context_var img_context_var %}
    """
    tokens = token.split_contents()
    size = len(tokens)

    if size < 2:
        msg = "Invalid number of arguments, found %s should be 1 or 2."
        raise template.TemplateSyntaxError(msg % (size-1))

    tagName = tokens[0]
    pages = tokens[1]
    img = ""
    if size == 3: img = tokens[2].strip("'").strip('"')
    pages = pages.strip("'").strip('"')
    log.debug("tagName: %s, pages: %s, img: %s", tagName, pages, img)
    return BreadcrumbNode(tagName, pages, img)


class BreadcrumbNode(template.Node):
    def __init__(self, tagName, pages, img=""):
        """
        First var is title, second var is url context variable
        """
        self._tagName = tagName
        self._pagesVar = template.Variable(pages)

        if img != "":
            self._imgVar = template.Variable(img)
        else:
            self._imgVar = img

    def render(self, context):
        try:
            locations = self._pagesVar.resolve(context)
        except:
            locations = eval(self._pagesVar.var)

        if not isinstance(self._imgVar, six.string_types):
            try:
                img = self._imgVar.resolve(context)
            except:
                img = self._imgVar.var
        else:
            img = self._imgVar

        log.debug("locations: %s, img: %s", locations, img)
        return self._createCrumbs(locations, img=img)

    def _createCrumbs(self, locations, img=""):
        """
        Assemble the breadcrumbs.
        """
        buff = six.StringIO()
        count = 0
        size = len(locations) - 1

        for title, url in locations:
            log.debug("title: %s, url: %s", title, url)
            # Make the last page non-linkable.
            if size == count: url = ""

            if count > 0:
                if img != "":
                    buff.write('<img class="arrow" src="%s" alt="&raquo;" />'\
                               % img)
                else:
                    buff.write('<span class="arrow">&raquo;</span>')

            if url:
                buff.write('<a class="title" href="%s">%s</a>' % (url, title))
            else:
                buff.write('<span class="title">%s</span>' % title)

            count += 1

        crumbs = buff.getvalue()
        buff.close()
        return crumbs
