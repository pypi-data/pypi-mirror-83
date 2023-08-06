"""Custom Exceptions."""
from auth_users.status_codes import StatusCodes as Status


class AuthRefreshTokenInvalid(Exception):
    def __init__(self, msg=None, status_code=None):
        if msg is None:
            msg = 'Refresh Token invalid.'
        if status_code is None:
            status_code = Status.UNAUTHORIZED
        super(AuthRefreshTokenInvalid, self).__init__(msg, status_code)


class AuthRefreshTokenExpired(Exception):
    def __init__(self, msg=None, status_code=None):
        if msg is None:
            msg = 'Refresh Token expired.'
        if status_code is None:
            status_code = Status.UNAUTHORIZED
        super(AuthRefreshTokenExpired, self).__init__(msg, status_code)
