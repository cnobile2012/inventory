#
# utils/exceptions.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2010-08-29 22:22:56 -0400 (Sun, 29 Aug 2010) $
# $Revision: 12 $
#----------------------------------

class InventoryException(Exception):
    __DEFAULT_MESSAGE = "Error: Default error message."

    def __init__(self, msg=__DEFAULT_MESSAGE):
        super(InventoryException, self).__init__(msg)
        
        if msg is None:
            msg = self.__DEFAULT_MESSAGE

        self.__message = msg

    def __str__(self):
        return self.__message

    def getMessage(self):
        return self.__message


class DoesNotExist(InventoryException):
    def __init__(self, msg):
        super(DoesNotExist, self).__init__(msg)
