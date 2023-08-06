import jwt

from .exceptions.invalid_token_exception import InvalidTokenException


class SimplerAuthenticator:
    def __init__(self, secret: str):
        self.secret = secret

    def create_user_unexpirable_token(self, user_id: str) -> str:
        token_bytes = jwt.encode(
            {"userId": user_id},
            self.secret,
            algorithm='HS256'
        )

        return str(token_bytes, 'utf-8')

    def get_user_id_from_unexpirable_token(self, token: str) -> str:
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms='HS256',
                options={'verify_signature': True, 'verify_exp': False}
            )
        except (
            jwt.exceptions.InvalidSignatureError,
            jwt.exceptions.DecodeError,
            UnicodeDecodeError
        ):
            raise InvalidTokenException('Invalid token')

        return payload['userId']
