"""
Client for the Genre resource of GiantBomb
"""
from pybomb.clients.base_client import BaseClient, ResponseParam


class GenreClient(BaseClient):
    """
    Client for the 'genre' API resource
    """
    RESOURCE_NAME = 'genre'

    RESPONSE_FIELD_MAP = {
        'api_detail_url': ResponseParam(True, False),
        'date_added': ResponseParam(True, False),
        'date_last_updated': ResponseParam(True, False),
        'deck': ResponseParam(True, False),
        'description': ResponseParam(True, False),
        'guid': ResponseParam(True, False),
        'id': ResponseParam(True, False),
        'image': ResponseParam(True, False),
        'name': ResponseParam(True, False),
        'site_detail_url': ResponseParam(True, False)
        }

    def fetch(self, id_, return_fields=None):
        """
        Wrapper for fetching details of genre by ID

        :param id_: int
        :param return_fields: tuple

        :return: pybomb.clients.Response
        """
        genre_params = {'id': id_}

        if return_fields is not None:
            self._validate_return_fields(return_fields)
            field_list = ','.join(return_fields)

            genre_params['field_list'] = field_list

        response = self._query(genre_params, direct=True)

        return response
