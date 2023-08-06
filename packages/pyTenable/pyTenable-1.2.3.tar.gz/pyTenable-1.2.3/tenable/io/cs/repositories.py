from tenable.base.endpoint import APIEndpoint
from .iterator import ConSecIterator

class RepositoriesAPI(APIEndpoint):
    _path = 'container-security/api/v2/repositories'

    def list(self, **kwargs):
        kwargs['imageName'] = kwargs.get('image_name')
        kwargs['nameContains'] = kwargs.get('name_contains')
        return ConSecIterator(self._api,
            limit=kwargs.get('limit', 1000),
            offset=kwargs.get('offset', 0),
            _params=kwargs,
            _path=self._path
        )

    def details(self, name):
        return self._get(name).content

    def delete(self, name):
        return self._delete(name)