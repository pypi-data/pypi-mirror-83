'''
Exclusions
==========

Methods described in this section relate to the the scan target exclusions API
under the vm section.  These methods can be accessed at
``TenableIO.vm.exclusions``.

.. rst-class:: hide-signature
.. autoclass:: ExclusionsAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from tenable.io.schemas.exclusions import ExclusionCreateSchema, ExclusionSchema


class ExclusionsAPI(APIEndpoint):
    _path = 'exclusions'

    def create(self, **kwargs):
        '''
        Creates a new scan target exclusion.

        :devportal:`Endpoint documentation <exclusions-create>`

        Args:
            name (str): The name of the exclusion to create.
            members (list):
                The exclusions members.  Each member should be a string with
                either a FQDN, IP Address, IP Range, or CIDR.
            description (str, optional):
                Some further detail about the exclusion.
            start_time (datetime): When the exclusion should start.
            end_time (datetime): When the exclusion should end.
            timezone (str, optional):
                The timezone to use for the exclusion.  The default if none is
                specified is to use UTC.  For the list of usable timezones,
                please refer to :devportal:`scans-timezones`
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
                The day of exclusionsthe month to repeat a **MONTHLY** frequency rule on.
                The default is today.
            enabled (bool, optional):
                Is the exclusion enabled?  The default is ``True``

        Returns:
            :obj:`dict`:
                Dictionary of the newly minted exclusion.

        Examples:
            Creating a one-time exclusion:

            >>> from datetime import datetime, timedelta
            >>> exclusion = tio.vm.exclusions.create(
            ...     'Example One-Time Exclusion',
            ...     ['127.0.0.1'],
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a daily exclusion:

            >>> exclusion = tio.vm.exclusions.create(
            ...     'Example Daily Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='daily',
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a weekly exclusion:

            >>> exclusion = tio.vm.exclusions.create(
            ...     'Example Weekly Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='weekly',
            ...     weekdays=['mo', 'we', 'fr'],
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a monthly esxclusion:

            >>> exclusion = tio.vm.exclusions.create(
            ...     'Example Monthly Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='monthly',
            ...     day_of_month=1,
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))

            Creating a yearly exclusion:

            >>> exclusion = tio.vm.exclusions.create(
            ...     'Example Yearly Exclusion',
            ...     ['127.0.0.1'],
            ...     frequency='yearly',
            ...     start_time=datetime.utcnow(),
            ...     end_time=datetime.utcnow() + timedelta(hours=1))
        '''
        schema = ExclusionCreateSchema()
        return self._post(json=schema.load(kwargs))

    def edit(self, id, **kwargs):
        '''
        Edit an existing scan target exclusion.

        :devportal:`Endpoint documentation <exclusions-edit>`

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
                The timezone to use for the exclusion.  The default if none is
                specified is to use UTC.
            frequency (str, optional):
                The frequency of the rule. The string inputted will be upcased.
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
            :obj:`dict`:
                Dictionary of the newly minted exclusion.

        Examples:
            Modifying the name of an exclusion:

            >>> exclusion = tio.vm.exclusions.edit(1, name='New Name')
        '''
        schema = ExclusionSchema()
        return self._put(json=schema.load(dict_merge(self.details(id), kwargs)))

    def list(self):
        '''
        List the currently configured scan target exclusions.

        :devportal:`Endpoint documentation <exclusions-list>`

        Returns:
            :obj:`list`:
                List of exclusion resource records.

        Examples:
            >>> for exclusion in tio.vm.exclusions.list():
            ...     pprint(exclusion)
        '''
        return self._get().exclusions

    def details(self, id):
        '''
        Retrieve the details for a specific scan target exclusion.

        :devportal:`Endpoint documentation <exclusions-details>`

        Args:
            id (int): The exclusion identifier.

        Returns:
            :obj:`dict`:
                The exclusion record requested.

        Examples:
            >>> exclusion = tio.vm.exclusions.details(1)
            >>> print(exclusion)
        '''
        return self._get(id)

    def delete(self, id):
        '''
        Delete a scan target exclusion.

        :devportal:`Endpoint documentation <exclusions-delete>`

        Args:
            id (int): The exclusion identifier to delete

        Returns:
            :obj:`None`:
                The exclusion was successfully deleted.

        Examples:
            >>> tio.vm.exclusions.delete(1)
        '''
        return self._delete(id)