"""
Client for the Theme resource of GiantBomb
"""
from base_client import BaseClient, ResponseParam


class ThemeClient(BaseClient):
    """
    Client for the 'theme' API resource
    """
    RESOURCE_NAME = 'theme'

    def fetch(self, id_):
        """
        Wrapper for fetching details of theme by ID

        :param id_: int
        :param return_fields: tuple

        :return: Response
        """
        theme_params = {'id': id_}

        response = self._query(theme_params, direct=True)

        return response
