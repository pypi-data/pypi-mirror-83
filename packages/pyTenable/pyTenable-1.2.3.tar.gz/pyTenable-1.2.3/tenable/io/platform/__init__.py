'''
Platform
========

.. toctree::
    :hidden:
    :glob:

    connectors
    groups
    session
    users

.. rst-class:: hide-signature
.. autoclass:: PlatformAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from .connectors import ConnectorsAPI
from .groups import GroupsAPI
from .session import SessionAPI
from .users import UsersAPI


class PlatformAPI(APIEndpoint):
    '''
    '''
    @property
    def connectors(self):
        '''
        The interface object for the :doc:`Connectors APIs <connectors>`.
        '''
        return ConnectorsAPI(self._api)

    @property
    def groups(self):
        '''
        The interface object for the :doc:`Groups APIs <groups>`.
        '''
        return GroupsAPI(self._api)

    @property
    def session(self):
        '''
        The interface object for the :doc:`Session APIs <session>`.
        '''
        return SessionAPI(self._api)

    @property
    def users(self):
        '''
        The interface object for the :doc:`Users APIs <users>`.
        '''
        return UsersAPI(self._api)