class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserNotFound(UserError):
    pass


class UserAlreadyRegistered(UserError):
    pass


class InvalidUsername(UserError):
    pass


class IncorrectPassword(UserError):
    pass

