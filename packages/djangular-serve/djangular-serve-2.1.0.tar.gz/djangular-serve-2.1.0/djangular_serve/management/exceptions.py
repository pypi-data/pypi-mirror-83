"""""
Error handler.
"""""


class ServeException(Exception):
    """""
    Exceptions
    """""
    pass


class ArgDoesNotExist(ServeException):
    """""
    Arg doesn't not exist
    """""

    def __init__(self, hint) -> None:
        if self.args is ArgDoesNotExist:
            raise ArgDoesNotExist(hint)


class ReqModuleNotExist(ServeException):
    """
    Missing module exception
    """
    def __init__(self, module):
        if self.args is ReqModuleNotExist:
            raise ReqModuleNotExist(module)


