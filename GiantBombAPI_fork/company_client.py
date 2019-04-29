"""
Client for the Company resource of GiantBomb
"""
from base_client import BaseClient, ResponseParam


class CompanyClient(BaseClient):
    """
    Client for the 'company' API resource
    """
    RESOURCE_NAME = 'company'

    def fetch(self, id_, return_fields=None):
        """
        Wrapper for fetching details of company by ID

        :param id_: int
        :param return_fields: tuple

        :return: Response
        """
        params = {'id': id_}

        response = self._query(params, direct=True)

        return response
