#
# utils/exceptions.py
#

class InventoryException(Exception):
    __DEFAULT_MESSAGE = "Error: Default error message."

    def __init__(self, msg=__DEFAULT_MESSAGE):
        super().__init__(msg)

        if msg is None:
            msg = self.__DEFAULT_MESSAGE

        self.__message = msg

    def __str__(self):
        return self.__message

    def getMessage(self):
        return self.__message


class DoesNotExist(InventoryException):
    def __init__(self, msg):
        super().__init__(msg)
