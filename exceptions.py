class Error(Exception):
    """Base class for other exceptions"""
    pass


class URLValidationError(Error):
    """Raised when the url is not validated"""
    pass
