class UserUnidentified(Exception):
    pass

class AuthenticationError(Exception):
    pass

class InternalError(Exception):
    pass

class BinanceServerError(Exception):
    pass

class BadRequestError(Exception):
    pass