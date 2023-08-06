'''
Assets
======

Methods described in this section relate to the the assets API under the vm
section.  These methods can be accessed at ``TenableIO.vm.assets``.

.. rst-class:: hide-signature
.. autoclass:: AssetsAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from marshmallow import Schema,fields, pre_load, post_load, validate as v
from tenable.io.schemas.filters import AssetsDeleteFilterSchema
from tenable.io.iterators import Version1Iterator


class AssetsDeleteSchema(Schema):
    _and = fields.Nested(AssetsDeleteFilterSchema, many=True)
    _or = fields.Nested(AssetsDeleteFilterSchema, many=True)
    base = fields.Nested(AssetsDeleteFilterSchema, data_key='filter')

    def load_filters(self, filters):
        for f in ['_and', '_or', 'base']:
            self.declared_fields[f].nested.filters = filters

    @post_load
    def reformat_output(self, data, **kwargs):
        print(data)
        resp = {'query': data.get('base')[0]}
        if data.get('_or'):
            resp['query']['or'] = data.get('_or')
        if data.get('_and'):
            resp['query']['and'] = data.get('_and')
        return resp


class AssignTagsSchema(Schema):
    action = fields.String(validate=v.OneOf(['add', 'remove']))
    assets = fields.List(fields.String(validate=
        v.Regexp('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')))
    tags = fields.List(fields.String(validate=
        v.Regexp('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')))


class AssetImportSchema(Schema):
    source = fields.String(required=True)
    assets = fields.List(fields.Dict(), required=True)


class AssetsAPI(APIEndpoint):
    _path = 'assets'

    def list(self):
        '''
        Returns a list of assets.

        :devportal:`Endpoint documentation <assets-list-assets>`

        Returns:
            :obj:`list`:
                List of asset records.

        Examples:
            >>> for asset in tio.vm.assets.list():
            ...     print(asset)
        '''
        return self._get().assets

    def delete(self, **kwargs):
        '''
        Deletes the asset.

        :devportal:`Endpoint documentation <assets-bulk-delete>`

        Args:
            id (str, optional):
                A single asset id.
            filter (tuple, optional):
                A filter tuple containing the condition for which to delete
                assets.
            _and (list[tuple], optional):
                A list of additional filter tuples.  These filters will be
                matched with a logical `and` within the API.
            _or (list[tuple], optional):
                A list of additional filter tuples.  These filters will be
                matched with a logical `or` within the API.

        Examples:
            Delete a single asset:

            >>> tio.vm.assets.delete(id=asset_id)

            Delete multiple assets based on a rule condition:

            >>> f = ('last_assessed', 'date-lt', '2020-03-13T16:24:25.290Z')
            >>> tio.vm.assets.delete(filter=f)

            Delete multiple assets using multiple filters:

            >>> f1 = ('last_assessed', 'date-lt', '2020-03-13T16:24:25.290Z')
            >>> f2 = ('network_id', 'eq', '00000000-0000-0000-0000-000000000000')
            >>> tio.vm.assets.delete(filter=f1, _and=[f2])
        '''
        if kwargs.get('id'):
            return self._api.delete(
                'workbenches/assets/{}'.format(kwargs.get('id'))
            )
        else:
            schema = AssetsDeleteSchema()
            schema.load_filters(self._api.vm.filters.workbench_assets())
            return self._post('bulk-jobs/delete',
                json=schema.load()
            ).response.data

    def details(self, id):
        '''
        Retrieves the details about a specific asset.

        :devportal:`Endpoint documentation <assets-asset-info>`

        Args:
            id (str):
                The unique identifier for the asset.

        Returns:
            :obj:`dict`:
                Asset resource definition.

        Examples:
            >>> id = '00000000-0000-0000-0000-000000000000'
            >>> asset = tio.vm.assets.details(id)
        '''
        return self._get(id)

    def assign_tags(self, **kwargs):
        '''
        Add/remove tags for asset(s).

        :devportal:`Endpoint documentation <tags-assign-asset-tags>`

        Args:
            action (str):
                Specifies whether to add or remove tags.
                Valid values: add, remove.
            assets (list[str]):
                An array of asset UUIDs.
            tags (list[str]):
                An array of tag value UUIDs.

        Returns:
            :obj:`dict`:
                The job Resource record.

        Examples:
            >>> asset = tio.vm.assets.assign_tags(
            ...     action='add',
            ...     assets=['00000000-0000-0000-0000-000000000000'],
            ...     tags=['00000000-0000-0000-0000-000000000000']
            ... )
        '''
        schema = AssignTagsSchema()
        return self._post('assignments', json=schema.load(kwargs))

    def tags(self, id):
        '''
        Retrieves the details about a specific asset.

        :devportal:`Endpoint documentation <tags-list-asset-tags>`

        Args:
            id (str):
                The unique identifier for the asset.

        Returns:
            :obj:`dict`:
                Asset resource definition.

        Examples:
            >>> id = '00000000-0000-0000-0000-000000000000'
            >>> asset = tio.vm.assets.tags(id)
        '''
        return self._get('{}/assignments'.format(id))

    def asset_import(self, **kwargs):
        '''
        Imports asset information into Tenable.io from an external source.

        :devportal:`Endpoint documentation <assets-import>`

        Imports a list of asset definition dictionaries.  Each asset record must
        contain at least one of the following attributes: ``fqdn``, ``ipv4``,
        ``netbios_name``, ``mac_address``.  Each record may also contain
        additional properties.

        Args:
            assets (list[dict]):
                The list of asset dictionaries
            source (str):
                An identifier to be used to upload the assets.

        Returns:
            :obj:`str`:
                The job UUID.

        Examples:
            >>> tio.vm.assets.asset_import(
            ...     source='example_source',
            ...     assets=[{
            ...         'fqdn': ['example.py.test'],
            ...         'ipv4': ['192.168.254.1'],
            ...         'netbios_name': 'example',
            ...         'mac_address': ['00:00:00:00:00:00']
            ...     }]
            ... )
        '''
        schema = AssetImportSchema()
        return self._api.post('import/assets',
            json=schema.load(kwargs)
        ).asset_import_job_uuid

    def list_import_jobs(self):
        '''
        Returns a list of asset import jobs.

        :devportal:`Endpoint documentation <assets-list-import-jobs>`

        Returns:
            :obj:`list`:
                List of job records.

        Examples:
            >>> for job in tio.vm.assets.list_import_jobs():
            ...     print(job)
        '''
        return self._api.get('import/asset-jobs').asset_import_jobs

    def import_job_details(self, id):
        '''
        Returns the details about a specific asset import job.

        :devportal:`Endpoint documentation <assets-import-job-info>`

        id (str):
            The unique identifier for the job.

        Returns:
            :obj:`dict`:
                The job Resource record.

        Examples:
            >>> id = '00000000-0000-0000-0000-000000000000'
            >>> job = tio.vm.assets.import_job_details(id)
            >>> print(job)
        '''
        return self._api.get('import/asset-jobs/{}'.format(id))