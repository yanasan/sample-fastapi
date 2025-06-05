class SAMPLEException(Exception):
    """Base exception for SAMPLE API"""
    pass


class AuthenticationException(SAMPLEException):
    """Authentication failed"""
    pass


class AuthorizationException(SAMPLEException):
    """Authorization failed"""
    pass


class NotFoundException(SAMPLEException):
    """Resource not found"""
    pass
