class UserMixin:
    """
    Defines the model of the `User` used by this framework.

    The application's User **MUST** inherit from this class and implement
    **ALL** the methods defined here.
    """

    def get_user_id(self) -> str:
        """
        Returns the `ID` of the `User`.

        :return: ID of the User.
        :rtype: str
        """

        raise NotImplementedError
