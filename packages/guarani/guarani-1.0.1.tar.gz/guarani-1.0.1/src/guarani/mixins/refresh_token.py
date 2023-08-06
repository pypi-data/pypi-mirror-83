from __future__ import annotations

from datetime import datetime


class RefreshTokenMixin:
    """
    Defines the model of the `Refresh Token` used by this framework.

    The application's Refresh Token **MUST** inherit from this class
    and implement **ALL** the methods defined here.
    """

    def get_refresh_token(self) -> str:
        """
        Returns the string that represents the `Refresh Token` object.

        :return: Refresh Token value.
        :rtype: str
        """

        raise NotImplementedError

    def get_client_id(self) -> str:
        """
        Returns the `ID` of the `Client` bound to the `Refresh Token`.

        :return: ID of the Client from this Refresh Token.
        :rtype: str
        """

        raise NotImplementedError

    def get_user_id(self) -> str:
        """
        Returns the `ID` of the `User` bound to the current `Refresh Token`.

        :return: ID of the User from this Refresh Token.
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

    def get_expiration(self) -> datetime:
        """
        Returns a datetime representing the expiration of the `Refresh Token`.

        :return: Time when the Refresh Token expires.
        :rtype: datetime
        """

        raise NotImplementedError
