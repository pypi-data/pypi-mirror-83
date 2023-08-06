'''
Agents
======

Methods described in this section relate to the the agents API under the vm
section.  These methods can be accessed at ``TenableIO.vm.agents``.

.. rst-class:: hide-signature
.. autoclass:: AgentsAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from tenable.io.iterators import Version1Iterator

class AgentsAPI(APIEndpoint):
    _path = 'scanners/1/agents'

    def list(self, **kwargs):
        '''
        Get the listing of configured agents from Tenable.io.

        :devportal:`Endpoint documentation <agents-list>`

        Args:
            filters (list[tuple], optional):
                Filters are tuples in the form of ('NAME', 'OPERATOR', 'VALUE').
                Multiple filters can be used and will filter down the data being
                returned from the API.

                Examples:
                    - ``('distro', 'match', 'win')``
                    - ``('name', 'nmatch', 'home')``

                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the `filters:agents <https://cloud.tenable.com/api#/resources/filters/agents-filters>`_
                endpoint to get more details.
            filter_type (str, optional):
                The filter_type operator determines how the filters are combined
                together.  ``and`` will inform the API that all of the filter
                conditions must be met for an agent to be returned, whereas
                ``or`` would mean that if any of the conditions are met, the
                agent record will be returned.
            limit (int, optional):
                The number of records to retrieve.  Default is 50
            offset (int, optional):
                The starting record to retrieve.  Default is 0.
            scanner_id (int, optional):
                The identifier the scanner that the agent communicates to.
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

            >>> for agent in tio.vm.agents.list():
            ...     print(agent)

            Retrieving all of the windows agents:

            >>> for agent in tio.vm.agents.list(('distro', 'match', 'win')):
            ...     print(agent)
        '''
        kwargs['filterset'] = self._api.vm.filters.agents()
        return Version1Iterator(
            api=self._api,
            path=self._path,
            resource='agents',
            **kwargs
        )

    def details(self, id):
        '''
        Retrieves the details of an agent.

        :devportal:`Endpoint documentation <agents-get>`

        Args:
            id (int):
                The identifier of the agent.

        Returns:
            :obj:`dict`:
                The agent dictionary record.

        Examples:
            >>> agent = tio.vm.agents.details(1)
            >>> print(agent)
        '''
        return self._get(id)

    def unlink(self, ids):
        '''
        Unlink one or multiple agents from the Tenable.io instance.

        :devportal:`Endpoint documentation <agents-delete>`

        Args:
            ids (list[str]):
                List of agent ids to delete.

        Returns:
            :obj:`dict` or :obj:`None`:
                If unlinking a singular agent, a :obj:`None` response will be
                returned.  If unlinking multiple agents, a :obj:`dict` response
                will be returned with a task record.

        Examples:
            Unlink a singular agent:

            >>> tio.vm.agents.unlink([1])

            Unlink many agents:

            >>> tio.vm.agents.unlink([1, 2, 3])
        '''
        if len(ids) == 1:
            # as only a singular agent_id was sent over, we can call the delete
            # API
            return self._delete(ids[0])
        else:
            # if multiple agent ids are passed, then we will pass the request
            # to the bulk processor.
            return self._post('_bulk/unlink', json={'items': ids})

    def task_status(self, id):
        '''
        Retrieves the current status of the task requested.

        :devportal:`Endpoint documentation <bulk-task-agent-status>`

        Args:
            id (str): The id of the agent task

        Returns:
            :obj:`dict`:
                Task resource

        Examples:
            >>> item = tio.agents.unlink([21, 22, 23])
            >>> task = tio.agent.task_status(item['task_uuid'])
            >>> print(task)
        '''
        return self._get('_bulk/{}'.format(id))
