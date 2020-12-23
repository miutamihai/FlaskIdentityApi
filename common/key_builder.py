import hashlib
import os


class KeyBuilder:
    @staticmethod
    def make_salt():
        return os.urandom(32)

    @staticmethod
    def make_key(salt, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
