from __future__ import annotations

from shiro.jwk import JsonWebKey


class ClientMixin:
    """
    Defines the model of the `Client` used by this framework.

    The application's Client **MUST** inherit from this class and implement
    **ALL** the methods defined here.
    """

    def get_client_id(self) -> str:
        """
        Returns the `ID` of the `Client`.

        :return: ID of the Client.
        :rtype: str
        """

        raise NotImplementedError

    def get_client_secret(self) -> str:
        """
        Returns the `Secret` of the `Client`.

        :return: Secret of the Client.
        :rtype: str
        """

        raise NotImplementedError

    def get_client_public_key(self, key_id: str) -> JsonWebKey:
        """
        Returns an instance of the Client's Public Key based on
        the provided Key ID or the default Public key.

        :param key_id: ID of the Public Key to be retrieved.
        :type key_id: str

        :return: Instance of the Client's (default) Public Key.
        :rtype: JsonWebKey
        """

        raise NotImplementedError

    def get_allowed_scopes(self, scopes: list[str]) -> list[str]:
        """
        Returns the `Scopes` that the `Client` is allowed to used
        based on the requested scopes.

        :param scopes: Requested scopes.
        :type scopes: list[str]

        :return: Scopes that the Client is allowed to request.
        :rtype: list[str]
        """

        raise NotImplementedError

    def get_redirect_uris(self) -> list[str]:
        """
        Returns a list of the `Redirect URIs` registered for the current `Client`.

        :return: Redirect URIs registered for the current Client.
        :rtype: list[str]
        """

        raise NotImplementedError

    def get_token_endpoint_auth_method(self) -> str:
        """
        Returns the `Token Endpoint Auth Method` of the `Client` stored in the database.

        :return: Token Endpoint Authentication Method of the Client.
        :rtype: str
        """

        raise NotImplementedError

    def get_grant_types(self) -> list[str]:
        """
        Returns a list of the `Grant Types` that the `Client` is allowed to request.

        :return: Grant Types that the Client is allowed to request.
        :rtype: list[str]
        """

        raise NotImplementedError

    def get_response_types(self) -> list[str]:
        """
        Returns a list of the `Response Types` that the `Client` is allowed to request.

        :return: Response Types that the Client is allowed to request.
        :rtype: list[str]
        """

        raise NotImplementedError
