from __future__ import annotations

from datetime import datetime


class AuthorizationCodeMixin:
    """
    Defines the model of the `Authorization Code` used by this framework.

    The application's Authorization Code **MUST** inherit from this class
    and implement **ALL** the methods defined here.
    """

    def get_client_id(self) -> str:
        """
        Returns the `ID` of the `Client` that requested the `Authorization Grant`.

        :return: ID of the Client from this Authorization Code.
        :rtype: str
        """

        raise NotImplementedError

    def get_user_id(self) -> str:
        """
        Returns the `ID` of the `User` that issued the current `Authorization Grant`.

        :return: ID of the User from this Authorization Code.
        :rtype: str
        """

        raise NotImplementedError

    def get_redirect_uri(self) -> str:
        """
        Returns the `Redirect URI` of the current `Authorization Code`.

        :return: Redirect URI.
        :rtype: str
        """

        raise NotImplementedError

    def get_scopes(self) -> list[str]:
        """
        Returns the `Scopes` that were authorized by the `User` to the `Client`.

        :return: Authorized Scopes.
        :rtype: list[str]
        """

        raise NotImplementedError

    def get_code_challenge(self) -> str:
        """
        Returns the `Code Challenge` provided by the `Client`.

        :return: Code Challenge.
        :rtype: str
        """

        raise NotImplementedError

    def get_code_challenge_method(self) -> str:
        """
        Returns the `Code Challenge Method` used by the `Client`.

        :return: Code Challenge Method.
        :rtype: str
        """

        raise NotImplementedError

    def get_nonce(self) -> str:
        """
        Returns the value of the `nonce` provided by the `Client`
        in the `Authentication Request`.

        :return: Nonce value of the Client.
        :rtype: str
        """

        raise NotImplementedError

    def get_auth_time(self) -> int:
        """
        Returns the time of the authentication of the User.

        :return: Time of User authentication.
        :rtype: int
        """

        raise NotImplementedError

    def get_expiration(self) -> datetime:
        """
        Returns a datetime representing the expiration of the `Authorization Code`.

        :return: Time when the Authorization Code expires.
        :rtype: datetime
        """

        raise NotImplementedError
