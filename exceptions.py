class AppError(Exception):
    """All errors come from here"""
    pass

class UsernameInUseError(AppError): pass