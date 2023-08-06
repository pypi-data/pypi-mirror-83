import pytest

from ..simpler_authenticator import SimplerAuthenticator
from ..exceptions.invalid_token_exception import InvalidTokenException


class TestSimplerAuthenticator:

    @pytest.fixture()
    def mocked_jwt(self, mocker):
        return mocker.patch('authventure.simpler_authenticator.jwt')

    def test_create_user_unexpirable_token(self):
        # Arrange
        expected_secret = 'secret'
        simpler_authenticator = SimplerAuthenticator(expected_secret)

        expected_user_id = 'f4K3-us3R-1234'
        expected_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.' \
                         'eyJ1c2VySWQiOiJmNEszLXVzM1ItMTIzNCJ9.' \
                         'H7_o6D55JV8SCvpRyl7p-fu0718qmy9XIvvTKyuhbpA'

        # Act
        token = simpler_authenticator.create_user_unexpirable_token(
            expected_user_id
        )

        # Assert
        assert token == expected_token

    def test_get_user_id_from_unexpirable_token(self, mocked_jwt):
        # Arrange
        token = 'f4K3.us3R.t0K3n'

        expected_user_id = 'f4K3-us3R-1234'
        expected_payload = {"userId": expected_user_id}

        mocked_jwt.decode.return_value = expected_payload

        expected_secret = 'secret'
        simpler_authenticator = SimplerAuthenticator(expected_secret)

        # Act
        user_id = simpler_authenticator.get_user_id_from_unexpirable_token(
            token
        )

        # Assert
        mocked_jwt.decode.assert_called_once_with(
            token,
            expected_secret,
            algorithms='HS256',
            options={'verify_signature': True, 'verify_exp': False}
        )

        assert user_id == expected_user_id

    def test_get_user_id_from_unexpirable_token_if_invalid_signature(self):
        # Arrange
        simpler_authenticator = SimplerAuthenticator('secret')

        # Assert
        with pytest.raises(InvalidTokenException):
            simpler_authenticator.get_user_id_from_unexpirable_token(
                'f4K3.us3R.t0K3n'
            )
