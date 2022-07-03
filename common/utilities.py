from passlib.hash import pbkdf2_sha512


class Utilities:
    @staticmethod
    def username_is_valid(username: str) -> bool:
        return True

    @staticmethod
    def hash_password(password: str) -> bool:
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def hashed_password_check(password: str, hashed_pass: str) -> bool:
        return pbkdf2_sha512.verify(password, hashed_pass)

