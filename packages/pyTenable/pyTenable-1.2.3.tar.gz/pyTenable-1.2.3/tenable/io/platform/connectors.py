'''
Connectors
==========

Methods described in this section relate to the the connectors API under the
platform section.  These methods can be accessed at
``TenableIO.platform.connectors``.

.. rst-class:: hide-signature
.. autoclass:: ConnectorsAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from restfly.utils import dict_merge
from tenable.io.iterators import Version1Iterator
from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class ScheduleSchema(Schema):
    units = fields.String(validate=OneOf(['days', 'hours', 'minutes', 'weeks']))
    value = fields.Integer()


class ConnectorSchema(Schema):
    name = fields.String()
    type = fields.String()
    network_uuid = fields.UUID()
    params = fields.Dict()
    schedule = fields.Nested(ScheduleSchema)


class ConnectorCreateSchema(ConnectorSchema):
    name = fields.String(required=True)
    type = fields.String(required=True)
    params = fields.Dict(required=True)


class ConnectorsAPI(APIEndpoint):
    _path = 'settings/connectors'

    def create(self, **kwargs):
        '''
        Creates a new connector

        :devportal:`Endpoint Documentation <connectors-create-connector>`

        Args:
            name (str):
                The name of the connector to create.
            type (str):
                The type of connector to create.
            network_uuid (str, optional):
                The network UUID to associate with the connector.
            params (dict):
                The parameters dictionary with the associated configuration
                values for the connector.
            schedule (dict, optional):
                The schedule dictionary informing the platform how often to run
                the conenctor.

        Examples:
            Creating a connector that runs every day:

            >>> tio.platform.connectors.create(
            ...     name='Test Connector',
            ...     type='aws',
            ...     params=settings_dict,
            ...     schedule={'units': 'days', 'value': 1}
            ... )
        '''
        payload = ConnectorCreateSchema().load(kwargs)
        return self._post(json=payload).connector

    def list(self, **kwargs):
        '''
        Retrieve the list of configured connectors.

        :devportal:`Endpoint Documentation <connectors-list-connector>`

        Args:
            sort (str, optional):
                The sort field and direction in a colon-delimetet format.

        Returns:
            :obj:`Iterator`:
                An iterator presenting the data to the caller.

        Examples:
            >>> for c in tio.platform.connectors.list():
            ...     print(c.name)
        '''
        return Version1Iterator(self._api,
            _path=self._path,
            _resource='connectors',
            _query=kwargs
        )

    def edit(self, id, **kwargs):
        '''
        Creates a new connector

        :devportal:`Endpoint Documentation <connectors-update-connector>`

        Args:
            id (str):
                The UUID of the connector to modify.
            name (str, optional):
                The name of the connector to create.
            type (str, optional):
                The type of connector to create.
            network_uuid (str, optional):
                The network UUID to associate with the connector.
            params (dict, optional):
                The parameters dictionary with the associated configuration
                values for the connector.
            schedule (dict, optional):
                The schedule dictionary informing the platform how often to run
                the conenctor.

        Returns:
            :obj:`dict`:
                The connector resource.

        Examples:
            Updating the connector name:

            >>> tio.platform.connectors.edit(uuid,
            ...     name='New Connector name',
            ... )
        '''
        payload = ConnectorSchema().load(dict_merge(self.details(id), kwargs))
        return self._put(id, json=payload).connector

    def details(self, id):
        '''
        Retrieves the details about a specific connector

        :devportal:`Endpoint Documentation <connectors-connector-details>`

        Args:
            id (str):
                The UUID of the connector to retrieve.

        Returns:
            :obj:`dict`:
                The connector resource.

        Examples:
            >>> c = tio.platform.connectors.details(uuid)
        '''
        return self._get(id).connector

    def delete(self, id):
        '''
        Deletes the specified connector.

        :devportal:`Endpoint Documentation <connectors-delete-connector>`

        Args:
            id (str):
                The UUID of the connector to delete.

        Returns:
            :obj:`None`

        Example:
            >>> tio.platform.connectors.delete(id)
        '''
        return self._delete(id)

    def run(self, id):
        '''
        Initiates an out-of-band import using the specified connector.

        Args:
            id (str):
                The UUID of the connector to run.

        Returns:
            :obj:`dict`:
                The connector resource.

        Examples:
            >>> tio.platform.connectors.run(uuid)
        '''
        return self._post('{}/import'.format(id))

    # NOTE: The AWS-cloudtrail API wasn't added here.  This API would need to
    #       be tested with a live AWS environment, which I currently don't have
    #       * /settings/connectors/aws/cloudtrails