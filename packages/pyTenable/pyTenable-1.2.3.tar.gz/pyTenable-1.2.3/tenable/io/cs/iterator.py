from restfly.iterator import APIIterator
from box import BoxList

class ConSecIterator(APIIterator):
    _path = None
    _params = dict()
    limit = 1000
    offset = 0

    def _get_page(self):
        params = self._params
        params['limit'] = self.limit
        params['offset'] = self.offset
        resp = self._api.get(self._path, params=params)
        self.page = BoxList.from_json(resp.content)
        self.offset += limit