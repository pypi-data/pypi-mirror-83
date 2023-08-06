class TplException(Exception):
    """
    Base Exception for tpljson module
    """
    pass


class TplUnmatched(TplException):
    pass


class TplOutOfOrder(TplException):
    pass


class TplJsonException(TplException):
    """
    Exception for when JSON error is encountered
    """
    pass