"""
Client for the Platform resource of GiantBomb
"""
from base_client import BaseClient, ResponseParam


class PlatformClient(BaseClient):
    """
    Client for the 'platform' API resource
    """
    RESOURCE_NAME = 'platform'

    def fetch(self, id_):
        """
        Wrapper for fetching details of theme by ID

        :param id_: int
        :param return_fields: tuple

        :return: Response
        """
        params = {'id': id_}

        response = self._query(params, direct=True)

        return response
