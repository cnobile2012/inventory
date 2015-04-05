#
# inventory/common/loghandlers.py
#
# See for original code:
#   http://codeinthehole.com/writing/a-deferred-logging-file-handler-for-django/
#

from logging import FileHandler
from logging.handlers import RotatingFileHandler
import os


class DeferredFileHandler(FileHandler):

    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        kwargs['delay'] = True
        FileHandler.__init__(self, "/dev/null", *args, **kwargs)

    def _open(self):
        self.baseFilename = self.filename
        return BaseFileHandler._open(self)


class DeferredRotatingFileHandler(RotatingFileHandler):

    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        kwargs['delay'] = True    
        RotatingFileHandler.__init__(self, "/dev/null", *args, **kwargs)

    def _open(self):
        self.baseFilename = self.filename
        return RotatingFileHandler._open(self)
