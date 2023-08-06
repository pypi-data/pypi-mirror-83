'''
Credentials
===========

Methods described in this section relate to the the managed credentials API
under the vm section.  These methods can be accessed at
``TenableIO.vm.credentials``.

.. rst-class:: hide-signature
.. autoclass:: CredentialsAPI
    :members:
'''
from tenable.utils import dict_merge
from tenable.base.endpoint import APIEndpoint
from tenable.io.iterators import Version1Iterator
from marshmallow import Schema,fields, pre_load, post_load, validate as v

class PermissionSchema(Schema):
    type = fields.String(validate=v.OneOf(['user', 'group']))
    permissions = fields.Integer(validate=v.OneOf([32, 64]))
    grantee_uuid = fields.String(
        validate=v.Regexp('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'))

    @pre_load
    def conversion_process(self, data, **kwargs):
        if isinstance(data, tuple):
            data = {
                'type': data[0],
                'permissions': data[1],
                'grantee_uuid': data[2]
            }
        perms = {'use': 32, 'edit': 64}
        if data.get('permissions') in perms:
            data['permissions'] = perms[data.get('permissions')]
        return data


class CredentialSchema(Schema):
    name = fields.String()
    description = fields.String()
    type = fields.String()
    settings = fields.Dict()
    permissions = fields.Nested(PermissionSchema)
    ad_hoc = fields.Boolean()

    @pre_load
    def conversion(self, data, **kwargs):
        reserved = [
            'name',
            'description',
            'ad_hoc',
            'type',
            'settings',
            'permissions'
        ]
        if not data.get('settings'):
            data['settings'] = dict()
        for key in data.keys():
            if key not in reserved:
                data['settings'][key] = data.pop(key)
        return data


class CredentialCreateSchema(Schema):
    name = fields.String(required=True)

class CredentialsAPI(APIEndpoint):
    _path = 'credentials'

    def create(self, **kwargs):
        '''
        Creates a new managed credential.

        :devportal:`Endpoint documentation <credentials-create>`

        Args:
            name (str):
                The name of the credential.
            type (str):
                The type of credential to create.  For a list of values refer to
                the output of the :py:meth:`types() <CredentialsAPI.types>`
                method.
            description (str, optional):
                A description for the credential.
            permissions (list, optional):
                A list of permissions (in either tuple or native dict format)
                detailing whom is allowed to use or edit this credential set.
                For the dictionary format, refer to the API docs.  The tuple
                format uses the customary ``(type, perm, uuid)`` format.

                Examples:
                    - ``('user', 32, user_uuid)``
                    - ``('group', 32, group_uuid)``
                    - ``('user', 'use', user_uuid)``

            **settings (dict, optional):
                Additional keywords passed will be added to the settings dict
                within the API call.  As this dataset can be highly variable,
                it will not be validated and simply passed as-is.

        Returns:
            :obj:`str`:
                The UUID of the newly created credential.

        Examples:
            >>> group_id = '00000000-0000-0000-0000-000000000000'
            >>> tio.vm.credentials.create('SSH Account', 'SSH',
            ...     permissions=[('group', 'use', group_id)],
            ...     username='user1',
            ...     password='sekretsquirrel',
            ...     escalation_account='root',
            ...     escalation_password='sudopassword',
            ...     elevate_privileges_with='sudo',
            ...     bin_directory='/usr/bin',
            ...     custom_password_prompt='')
        '''
        schema = CredentialCreateSchema()
        return self._post(json=schema.load(kwargs))

    def edit(self, id, **kwargs):
        '''
        Creates a new managed credential.

        :devportal:`Endpoint documentation <credentials-create>`

        Args:
            id (str):
                The unique identifier of the managed credential.
            ad_hoc (bool, optional):
                Determins whether the credential is managed (``False``) or an
                embedded credential in a scan or policy (``True``).
            name (str, optional):
                The name of the credential.
            description (str, optional):
                A description for the credential.
            permissions (list, optional):
                A list of permissions (in either tuple or native dict format)
                detailing whom is allowed to use or edit this credential set.
                For the dictionary format, refer to the API docs.  The tuple
                format uses the customary ``(type, perm, uuid)`` format.

                Examples:
                    - ``('user', 32, user_uuid)``
                    - ``('group', 32, group_uuid)``
                    - ``('user', 'use', user_uuid)``

            **settings (dict, optional):
                Additional keywords passed will be added to the settings dict
                within the API call.  As this dataset can be highly variable,
                it will not be validated and simply passed as-is.

        Returns:
            :obj:`bool`:
                The status of the update process.

        Examples:
            >>> cred_uuid = '00000000-0000-0000-0000-000000000000'
            >>> tio.vm.credentials.edit(cred_uuid,
            ...     password='sekretsquirrel',
            ...     escalation_password='sudopassword')
        '''
        current = self.details(id)
        schema = CredentialSchema()
        return self._put(json=schema.load(dict_merge(current, kwargs)))

    def details(self, id):
        '''
        Retrives the details of the specified credential.

        :devportal:`Endpoint documentation <credentials-details>`

        Args:
            id (str): The UUID of the credential to retreive.

        Returns:
            :obj:`dict`:
                The resource record for the credential.

        Examples:
            >>> cred_uuid = '00000000-0000-0000-0000-000000000000'
            >>> cred = tio.vm.credentials.details(cred_uuid)
        '''
        return self._get(id)

    def delete(self, id):
        '''
        Deletes the specified credential.

        :devportal:`Endpoint documentation <credentials-delete>`

        Args:
            id (str): The UUID of the credential to retreive.

        Returns:
            :obj:`bool`:
                The status of the action.

        Examples:
            >>> cred_uuid = '00000000-0000-0000-0000-000000000000'
            >>> cred = tio.vm.credentials.delete(cred_uuid)
        '''
        return self._delete(id)

    def types(self):
        '''
        Lists all of the available credential types.

        :devportal:`Endpoint documentation <credentials-list-credential-types>`

        Returns:
            :obj:`list`:
                A list of the available credential types and definitions.

        Examples:
            >>> cred_types = tio.vm.credentials.types()
        '''
        return self._get('types')

    def list(self, **kwargs):
        '''
        Get the listing of configured credentials from Tenable.io.

        :devportal:`credentials: list <credentials-list>`

        Args:
            *filters (tuple, optional):
                Filters are tuples in the form of ('NAME', 'OPERATOR', 'VALUE').
                Multiple filters can be used and will filter down the data being
                returned from the API.

                Examples:
                    - ``('name', 'eq', 'example')``

                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth:`tio.filters.networks_filters() <FiltersAPI.networks_filters>`
                endpoint to get more details.
            filter_type (str, optional):
                The filter_type operator determines how the filters are combined
                together.  ``and`` will inform the API that all of the filter
                conditions must be met for an access group to be returned,
                whereas ``or`` would mean that if any of the conditions are met,
                the access group record will be returned.
            limit (int, optional):
                The number of records to retrieve.  Default is 50
            offset (int, optional):
                The starting record to retrieve.  Default is 0.
            owner_uuid (str, optional):
                The UUID of the scan owner.  If specified it will limit the
                responses to credentials assigned to scans owned by the
                specified user UUID.
            sort (tuple, optional):
                A tuple of tuples identifying the the field and sort order of
                the field.
            wildcard (str, optional):
                A string to pattern match against all available fields returned.
            wildcard_fields (list, optional):
                A list of fields to optionally restrict the wild-card matching
                to.

        Returns:
            :obj:`CredentialsIterator`:
                An iterator that handles the page management of the requested
                records.

        Examples:
            >>> for cred in tio.credentials.list():
            ...     pprint(cred)
        '''
        kwargs['filterset'] = self._api.vm.filters.networks()
        return Version1Iterator(
            api=self._api,
            path=self._path,
            resource='agents',
            **kwargs
        )