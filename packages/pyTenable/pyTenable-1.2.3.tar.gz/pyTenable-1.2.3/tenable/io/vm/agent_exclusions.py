'''
Agent Exclusions
================

Methods described in this section relate to the the agent exclusions API under
the vm section.  These methods can be accessed at
``TenableIO.vm.agent_exclusions``.

.. rst-class:: hide-signature
.. autoclass:: AgentExclusionsAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from tenable.io.schemas.exclusions import ExclusionCreateSchema, ExclusionSchema


class AgentExclusionsAPI(APIEndpoint):
    _path = 'scanners/1/agents/exclusions'

    def create(self, **kwargs):
        '''
        Creates a new agent exclusion.

        :devportal:`Endpoint documentation <agent-exclusions-create>`

        Args:
            name (str): The name of the exclusion to create.
            description (str, optional):
                Some further detail about the exclusion.
            start_time (datetime): When the exclusion should start.
            end_time (datetime): When the exclusion should end.
            timezone (str, optional):
                The timezone to use for the exclusion.  The default if none is
                specified is to use UTC.  For the list of usable timezones,
                please refer to:
                https://cloud.tenable.com/api#/resources/scans/timezones
            frequency (str, optional):
                The frequency of the rule. The string inputted will be up-cased.
                Valid values are: ``ONETIME``, ``DAILY``, ``WEEKLY``,
                ``MONTHLY``, ``YEARLY``.
                Default value is ``ONETIME``.
            interval (int, optional):
                The interval of the rule.  The default interval is 1
            weekdays (list, optional):
                List of 2-character representations of the days of the week to
                repeat the frequency rule on.  Valid values are:
                *SU, MO, TU, WE, TH, FR, SA*
                Default values: ``['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']``
            day_of_month (int, optional):
                The day of the month to repeat a **MONTHLY** frequency rule on.
                The default is today.
            enabled (bool, optional):
                Is the exclusion enabled?  The default is ``True``

        Returns:
            dict: Dictionary of the newly minted exclusion.

        Examples:
            Creating a one-time exclusion:

            >>> from datetime import datetime, timedelta
            >>> exclusion = tio.vm.agent_exclusions.create(
            ...     'Example One-Time Agent Exclusion',
            ...     ['127.0.0.1'],
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a daily exclusion:

            >>> exclusion = tio.vm.agent_exclusions.create(
            ...     'Example Daily Agent Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='daily',
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a weekly exclusion:

            >>> exclusion = tio.vm.agent_exclusions.create(
            ...     'Example Weekly Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='weekly',
            ...     weekdays=['mo', 'we', 'fr'],
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a monthly esxclusion:

            >>> exclusion = tio.vm.agent_exclusions.create(
            ...     'Example Monthly Agent Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='monthly',
            ...     day_of_month=1,
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a yearly exclusion:

            >>> exclusion = tio.vm.agent_exclusions.create(
            ...     'Example Yearly Agent Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='yearly',
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))
        '''
        schema = ExclusionCreateSchema()
        return self._post(json=schema.load(kwargs))

    def edit(self, id, **kwargs):
        '''
        Edit an existing agent exclusion.

        :devportal:`Endpoint documentation <agent-exclusions-edit>`

        The edit function will first gather the details of the exclusion that
        will be edited and will overlay the changes on top.  The result will
        then be pushed back to the API to modify the exclusion.

        Args:
            id (int): The id of the exclusion object in Tenable.io
            name (str, optional): The name of the exclusion to create.
            description (str, optional):
                Some further detail about the exclusion.
            start_time (datetime, optional): When the exclusion should start.
            end_time (datetime, optional): When the exclusion should end.
            timezone (str, optional):
                The timezone to use for the exclusion.
            frequency (str, optional):
                The frequency of the rule. The string inputted will be up-cased.
                Valid values are: *ONETIME, DAILY, WEEKLY, MONTHLY, YEARLY*.
            interval (int, optional): The interval of the rule.
            weekdays (list, optional):
                List of 2-character representations of the days of the week to
                repeat the frequency rule on.  Valid values are:
                *SU, MO, TU, WE, TH, FR, SA*
                Default values: ``['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']``
            day_of_month (int, optional):
                The day of the month to repeat a **MONTHLY** frequency rule on.

        Returns:
            dict: Dictionary of the newly minted exclusion.

        Examples:
            >>> exclusion = tio.vm.agent_exclusions.edit(1, name='New Name')
        '''
        schema = ExclusionSchema()
        return self._put(json=schema.load(dict_merge(self.details(id), kwargs)))

    def list(self):
        '''
        Lists all of the currently configured agent exclusions.

        :devportal:`Endpoint documentation <agent-exclusions-list>`

        Returns:
            list: List of agent exclusions.

        Examples:
            >>> for exclusion in tio.vm.agent_exclusions.list():
            ...     print(exclusion)
        '''
        return self._get().exclusions

    def details(self, id):
        '''
        Retrieve the details for a specific agent exclusion.

        :devportal:`Endpoint documentation <agent-exclusions-details>`

        Args:
            id (int): The id of the exclusion object in Tenable.io

        Returns:
            dict: The exclusion resource dictionary.

        Examples:
            >>> exclusion = tio.vm.agent_exclusions.details(1)
        '''
        return self._get(id)

    def delete(self, id):
        '''
        Delete an agent exclusion.

        :devportal:`Endpoint documentation <agent-exclusions-delete>`

        Args:
            id (int): The id of the exclusion object in Tenable.io

        Returns:
            None: The Exclusion was successfully deleted

        Examples:
            >>> tio.vm.agent_exclusions.delete(1)
        '''
        return self._delete(id)