'''
Access Groups
=============

Methods described in this section relate to the the access groups API under the
vm section.  These methods can be accessed at
``TenableIO.vm.access_groups``.

.. rst-class:: hide-signature
.. autoclass:: AccessGroupsAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from tenable.io.schemas.filters import AccessGroupsFilterSchema
from tenable.io.iterators import Version1Iterator
from tenable.utils import dict_merge
from marshmallow import Schema, fields, pre_load, post_load, EXCLUDE
from marshmallow.validate import OneOf
from uuid import UUID


class PrincipalSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    type = fields.String(validate=OneOf(['user', 'group']))
    principal_id = fields.UUID()
    principal_name = fields.String()

    @pre_load
    def serialize_tuple(self, item, **kwargs):
        '''
        This method will convert a tuple into the disctionary structure that
        will be validated and passed to the API.
        '''
        if isinstance(item, tuple):
            conv = {'type': item[0]}
            try:
                conv['principal_id'] = UUID(item[1])
            except ValueError:
                conv['principal_name'] = item[1]
            return conv
        return item

    @post_load
    def convert_principal_id_to_string(self, item, **kwargs):
        '''
        Converts the principal_id attribute to a string representation of the
        UUID identifier.
        '''
        if item.get('principal_id'):
            item['principal_id'] = str(item['principal_id'])
        return item


class AccessGroupRulesSchema(Schema):
    type = fields.String()
    operator = fields.String()
    terms = fields.List(fields.String())


class AccessGroupSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    name = fields.String()
    all_users = fields.Boolean()
    all_assets = fields.Boolean()
    principals = fields.List(fields.Nested(PrincipalSchema))
    rules = fields.List(fields.Dict())

    @pre_load
    def convert_inputs(self, data, **kwargs):
        '''
        Performs some simple conversion of the inputs to the expected field
        names used by the API.
        '''
        # Perform the filter conversion and validation.  If a filterset was
        # provided are part of the input, then we will also pull that out and
        # pass it into the filter schema.
        agrules = AccessGroupsFilterSchema()
        agrules.load_filters(self._api.vm.filters.access_group_asset_rules())
        if data.get('rules'):
            r = agrules.load(data.get('rules'))
            data['rules'] = r['rules']

        # return the transformed data back to the Schema.
        return data


class AccessGroupCreateSchema(AccessGroupSchema):
    name = fields.String(required=True)
    all_users = fields.Boolean(default=False)


class AccessGroupsAPI(APIEndpoint):
    _path = 'access-groups'

    def create(self, **krargs):
        '''
        Creates a new access group

        :devportal:`Endpoint documentation <access-groups-create>`

        Args:
            name (str):
                The name of the access group to create.
            rules (list):
                a list of rule tuples.  Tuples are defined in the standardized
                method of name, operator, value.  For example:

                .. code-block:: python

                    ('operating_system', 'eq', ['Windows NT'])

                Rules will be validate against by the filters before being sent
                to the API.  Note that the value field in this context is a list
                of string values.
            principals (list, optional):
                A list of principal tuples.  Each tuple must contain both the
                type and the identifier for the principal.  The identifier can
                be either a UUID associated to a user/group, or the name of the
                user/group.  For example:

                .. code-block:: python

                    ('user', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4')
                    ('user', 'steve@company.tld')
                    ('group', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4')

            all_users (bool, optional):
                If enabled, the access group will apply to all users and any
                principals defined will be ignored.

        Returns:
            :obj:`dict`:
                The resource record for the new access list.

        Examples:
            Allow all users to see 192.168.0.0/24:

            >>> tio.vm.access_groups.create('Example',
            ...     [('ipv4', 'eq', ['192.168.0.0/24'])],
            ...     all_users=True)

            Allow everyone in a specific group id to see specific hosts:

            >>> tio.vm.access_groups.create('Example',
            ...     [('netbios_name', 'eq', ['dc1.company.tld']),
            ...      ('netbios_name', 'eq', ['dc2.company.tld'])],
            ...     principals=[
            ...         ('group', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4')
            ... ])
        '''
        schema = AccessGroupCreateSchema()
        return self._post(json=schema.load(kwargs))

    def edit(self, id, **kwargs):
        '''
        Edits an access group

        :devportal:`Endpoint documentation <access-groups-edit>`

        Args:
            id (str):
                The UUID of the access group to edit.
            name (str, optional):
                The name of the access group to create.
            rules (list, optional):
                a list of rule tuples.  Tuples are defined in the standardized
                method of name, operator, value.  For example:

                .. code-block:: python

                    ('operating_system', 'eq', ['Windows NT'])

                Rules will be validate against by the filters before being sent
                to the API.  Note that the value field in this context is a list
                of string values.
            principals (list, optional):
                A list of principal tuples.  Each tuple must contain both the
                type and the identifier for the principal.  The identifier can
                be either a UUID associated to a user/group, or the name of the
                user/group.  For example:

                .. code-block:: python

                    ('user', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4')
                    ('user', 'steve@company.tld')
                    ('group', '32a0c314-442b-4aed-bbf5-ba9cf5cafbf4')

            all_users (bool, optional):
                If enabled, the access group will apply to all users and any
                principals defined will be ignored.
            all_assets (bool, optional):
                Specifies if the access group to modify is the default
                "all assets" group or a user-defined one.
        '''
        details = self.details(id)
        schema = AccessGroupSchema()
        return self._put(id,
            json=schema.load(dict_merge(self.details(id), kwargs))
        )

    def delete(self, id):
        '''
        Deletes the specified access group.

        :devportal:`Endpoint documentation <access-groups-delete>`

        Args:
            id (str): The UUID of the access group to remove.
        '''
        return self._delete(id)

    def details(self, id):
        '''
        Retrieves the details of the specified access group.

        :devportal:`Endpoint documentation <access-groups-details>`

        Args:
            id (str): The UUID of the access group.
        '''
        return self._get(id)

    def list(self, **kwargs):
        '''
        Get the listing of configured access groups from Tenable.io.

        :devportal:`Endpoint documentation <access-groups-list>`

        Args:
            filters (list, optional):
                Filters are tuples in the form of ('NAME', 'OPERATOR', 'VALUE').
                Multiple filters can be used and will filter down the data being
                returned from the API.

                Examples:
                    - ``('distro', 'match', 'win')``
                    - ``('name', 'nmatch', 'home')``

                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth:`tio.vm.filters.access_groups() <FiltersAPI.access_groups>`
                endpoint to get more details.
            filter_type (str, optional):
                The filter_type operator determines how the filters are combined
                together. ``and`` will inform the API that all of the filter
                conditions must be met for an access group to be returned,
                whereas ``or`` would mean that if any of the conditions are met,
                the access group record will be returned.
            limit (int, optional):
                The number of records to retrieve.  Default is 50
            offset (int, optional):
                The starting record to retrieve.  Default is 0.
            sort (tuple, optional):
                A tuple of tuples identifying the the field and sort order of
                the field.
            wildcard (str, optional):
                A string to pattern match against all available fields returned.
            wildcard_fields (list, optional):
                A list of fields to optionally restrict the wild-card matching
                to.

        Returns:
            :obj:`Version1Iterator`:
                An iterator that handles the page management of the requested
                records.

        Examples:
            Getting the listing of all agents:

            >>> for group in tio.access_groups.list():
            ...     print(group)

            Retrieving all of the windows agents:

            >>> groups = tio.vm.access_groups.list(filters=[('name', 'eq', 'win')])
            >>> for group in groups:
            ...     print(group)
        '''
        kwargs['filterset'] = self._api.vm.filters.access_groups()
        return Version1Iterator(
            api=self._api,
            path=self._path,
            resource='access_groups',
            **kwargs
        )