from tenable.base.endpoint import APIEndpoint
from .images import ImagesAPI
from .repositories import RepositoriesAPI


class ConSecAPI(APIEndpoint):
    @property
    def images(self):
        '''
        '''
        return ImagesAPI(self._api)

    @property
    def repositories(self):
        '''
        '''
        return RepositoriesAPI(self._api)