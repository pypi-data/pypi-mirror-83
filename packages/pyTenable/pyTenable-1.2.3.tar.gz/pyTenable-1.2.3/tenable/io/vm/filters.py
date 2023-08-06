'''
Filters
=======

Methods described in this section relate to the the filters API under the vm
section.  These methods can be accessed at
``TenableIO.vm.filters``.

.. rst-class:: hide-signature
.. autoclass:: FiltersAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint


def fmt_filters(fset):
    '''
    Converts the filters into an easily parsable dictionary.

    Args:
        fset (list):
            The raw filter list from the API.

    Returns:
        :type:`dict`:
            A key-value store of the filters with the filter attributes
            normalized based on regex pattern and choices available for the
            filter.
    '''
    filters = dict()
    for item in fset:
        f = {
            'operators': item['operators'],
            'choices': None,
            'pattern': None,
        }

        # If there is a list of choices available, then we need to parse
        # them out and only pull back the usable values as a list
        if 'list' in item['control']:
            # There is a lack of consistency here.  In some cases the "list"
            # is a list of dictionary items, and in other cases the "list"
            # is a list of string values.
            if isinstance(item['control']['list'][0], dict):
                key = 'value' if 'value' in item['control']['list'][0] else 'id'
                f['choices'] = [str(i[key]) for i in item['control']['list']]
            elif isinstance(item['control']['list'], list):
                f['choices'] = [str(i) for i in item['control']['list']]
        if 'regex' in item['control']:
            f['pattern'] = item['control']['regex']
        filters[item['name']] = f
    return filters


class FiltersAPI(APIEndpoint):
    _filter_cache = dict()

    def _cache(self, name, path, envelope='filters', fmt=True):
        '''
        Caches filtersets on demand and then returns the filterset to the caller
        in either a dictionary format typically used by the library, or as the
        raw response list.

        Args:
            name (str):
                The name of the cache to check.
            path (str):
                The URI path to get the filterset.
            envelope (str, optional):
                The name of the envelope containing the filter list.  If left
                unspecified, the default is to use the "filters" key for the
                envelope.
            fmt (bool, optional):
                Should the filters be converted to a key/value dictionary?  If
                left unspecified, the default is ``True``.
        '''
        if name not in self._filter_cache:
            self._filter_cache[name] = self._api.get(path)[envelope]

        if fmt:
            return fmt_filters(self._filter_cache[name])
        else:
            return self._filter_cache[name]

    def access_group_asset_rules(self, fmt=True):
        '''
        Returns access group rules filters.

        :devportal:`Endpoint Documentation <access-groups-list-rule-filters>`

        Args:
            fmt (bool, optional):
                Should the filters be converted to a key/value dictionary?  If
                left unspecified, the default is ``True``.

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.vm.filters.access_group_rules()
        '''
        return self._cache(
            'access_group_asset_rules',
            'access-groups/rules/filters',
            envelope='rules',
            fmt=fmt
        )

    def access_groups(self, fmt=True):
        '''
        Returns access group filters.

        :devportal:`Endpoint Documentation <access-groups-list-filters>`

        Args:
            fmt (bool, optional):
                Should the filters be converted to a key/value dictionary?  If
                left unspecified, the default is ``True``.

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.vm.filters.access_groups()
        '''
        return self._cache(
            'access_groups',
            'access-groups/filters',
            fmt=fmt
        )

    def agents(self, fmt=True):
        '''
        Returns agent filters.

        :devportal:`Endpoint Documentation <filters-agents-filters>`

        Args:
            fmt (bool, optional):
                Should the filters be converted to a key/value dictionary?  If
                left unspecified, the default is ``True``.

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.vm.filters.agents()
        '''
        return self._cache('agents', 'filters/scans/agents', fmt=fmt)

    def workbench_vulns(self, fmt=True):
        '''
        Returns the vulnerability workbench filters

        :devportal:`Endpoint Documentation <workbenches-vulnerabilities-filters>`

        Args:
            fmt (bool, optional):
                Should the filters be converted to a key/value dictionary?  If
                left unspecified, the default is ``True``.

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.vm.filters.workbench_vulns()
        '''
        return self._cache(
            'vulns', 'filters/workbenches/vulnerabilities', fmt=fmt)

    def workbench_assets(self, fmt=True):
        '''
        Returns the asset workbench filters.

        :devportal:`Endpoint Documentation <filters-assets-filter>`

        Args:
            fmt (bool, optional):
                Should the filters be converted to a key/value dictionary?  If
                left unspecified, the default is ``True``.

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.vm.filters.workbench_assets()
        '''
        return self._cache(
            'asset', 'filters/workbenches/assets', fmt=fmt)

    def scans(self, fmt=True):
        '''
        Returns the individual scan filters.

        Args:
            fmt (bool, optional):
                Should the filters be converted to a key/value dictionary?  If
                left unspecified, the default is ``True``.

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.vm.filters.scan_filters()
        '''
        return self._cache('scan', 'filters/scans/reports', fmt=fmt)

    def credentials(self, fmt=True):
        '''
        Returns the individual scan filters.

        :devportal:`filters: credentials <credentials-filters>`

        Args:
            fmt (bool, optional):
                Should the filters be converted to a key/value dictionary?  If
                left unspecified, the default is ``True``.

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.vm.filters.scan_filters()
        '''
        return self._cache('scan', 'filters/credentials', fmt=fmt)

    def networks(self):
        '''
        Returns the networks filters.

        Returns:
            :obj:`dict`:
                Filter resource dictionary

        Examples:
            >>> filters = tio.filters.networks()
        '''
        return {'name': {
            'operators': ['eq', 'neq', 'match'],
            'choices': None,
            'pattern': None
        }}
