from __future__ import annotations

from guarani.adapter import BaseAdapter
from guarani.authentication import ClientAuthentication
from guarani.configuration import Configuration
from guarani.models import Request, Response


class BaseEndpoint:
    """
    Base class for the endpoints of the OAuth 2.1 framework and its extensions.

    Any endpoint being implemented by the application or by extensions **MUST**
    inherit from this class and implement its abstract methods.

    The type, status, headers and body of the response it returns,
    as well as its meaning and formatting have to be documented
    by the respective endpoint.

    The method :meth:`create_response` **MUST NOT** raise exceptions.
    It **MUST** catch the exceptions and return a valid error response instead.

    :cvar `__endpoint__`: Name of the endpoint.

    :param adapter: Adapter registered within the Provider.
    :type adapter: BaseAdapter

    :param config: Configuration data of the Provider.
    :type config: Configuration

    :param authenticate: Object used to authenticate the current Client.
    :type authenticate: ClientAuthentication
    """

    __endpoint__: str = None

    def __init__(
        self,
        adapter: BaseAdapter,
        config: Configuration,
        authenticate: ClientAuthentication,
    ) -> None:
        self.adapter = adapter
        self.config = config
        self.authenticate = authenticate

    async def __call__(self, request: Request) -> Response:
        """
        All endpoints are required to implement this method,
        since it MUST return a response back to the client.

        The type, status, headers and body of the response it returns,
        as well as its meaning and formatting have to be documented by
        the respective endpoint.

        This method **MUST NOT** raise **ANY** exception.

        If an error occurred during the processing of the request,
        it **MUST** be treated and its appropriate response status,
        headers and body **MUST** be correctly set
        to denote the type of exception that occured.

        Other than the previous requirements, the endpoint is free
        to use whatever tools, methods and workflows it wished.

        It is recommended to split the logic of the endpoint into small
        single-responsibility methods for better maintenance.

        :param request: Current request being processed.
        :type request: Request

        :return: Response containing all the necessary info to the client.
        :rtype: Response
        """

        raise NotImplementedError
