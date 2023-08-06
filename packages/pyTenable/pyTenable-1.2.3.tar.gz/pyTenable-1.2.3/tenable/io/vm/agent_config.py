'''
Agent Config
============

Methods described in this section relate to the the agent config API under the
vm section.  These methods can be accessed at
``TenableIO.vm.agent_config``.

.. rst-class:: hide-signature
.. autoclass:: AgentConfigAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from marshmallow import Schema, fields, pre_load, validate


class AutoUnlinkSchema(Schema):
    enabled = fields.Boolean()
    expiration = fields.Integer(validate=validate.Range(1, 365))


class AgentConfigSchema(Schema):
    software_update = fields.Boolean()
    auto_unlink = fields.Nested(AutoUnlinkSchema)

    @pre_load
    def conversion(self, data, **kwargs):
        '''
        Perform any data conversions before validation.
        '''
        # if the auto_unlink is either a boolean or integer value, then we will
        # want to convert it into the expected dictionary object first.
        if isinstance(data.get('auto_unlink'), (bool, int)):
            if data.get('auto_unlink') == False:
                data['auto_unlink'] = {'enabled': False}
            elif isinstance(data.get('auto_unlink'), int):
                data['auto_unlink'] = {
                    'enabled': True,
                    'expiration': data.get('auto_unlink')
                }
        return data


class AgentConfigAPI(APIEndpoint):
    _path = 'scanners/1/agents/config'

    def edit(self, **kwargs):
        '''
        Modify the agent configuration.

        :devportal:`Endpoint documentation <agent-config-details>`

        Args:
            software_update (bool, optional):
                If True, software updates are enabled for agents (exclusions may
                override this).  If false, software updates for all agents are
                disabled.
            auto_unlink (int, optional):
                If true, agent auto-unlinking is enabled, allowing agents to
                automatically unlink themselves after a given period of time.
                If the value is 0 or false, auto-unlinking is disabled.  True
                values are between 1 and 365.

        Returns:
            :obj:`dict`:
                Dictionary of the applied settings is returned if successfully
                applied.

        Examples:
            Enabling auto-unlinking for agents after 30 days:

            >>> tio.vm.agent_config.edit(auto_unlink=30)

            Disabling auto-unlinking for agents:

            >>> tio.vm.agent_config.edit(auto_unlink=False)

            Enabling software updates for agents:

            >>> tio.vm.agent_config.edit(software_update=True)
        '''
        schema = AgentConfigSchema()
        return self._put(json=schema.load(kwargs))

    def details(self):
        '''
        Returns the current agent configuration.

        :devportal:`Endpoint documentation <agent-config-edit>`

        Args:
            scanner_id (int, optional): The scanner ID.

        Returns:
            :obj:`dict`:
                Dictionary of the current settings.

        Examples:
            >>> details = tio.vm.agent_config.details()
            >>> print(details)
        '''
        return self._get()