'''
Groups
======

Methods described in this section relate to the the user-groups API under the
platform section.  These methods can be accessed at
``TenableIO.platform.groups``.

.. rst-class:: hide-signature
.. autoclass:: GroupsAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from tenable.utils import dict_merge


class GroupsAPI(APIEndpoint):
    _path = 'groups'

    def add_user(self, group_is, user_id):
        '''
        Add a user to a user group.

        :devportal:`Endpoint Documentation <groups-add-user>`

        Args:
            group_id (int):
                The unique identifier of the group to add the user to.
            user_id (int):
                The unique identifier of the user to add.

        Returns:
            :obj:`None`:
                The user was successfully added to the group.

        Examples:
            >>> tio.platform.groups.add_user(1, 1)
        '''
        self._post('{}/users/{}'.format(group_id, user_id))

    def create(self, name):
        '''
        Create a new user group.

        :devportal:`Endpoint Documentation <groups-create>`

        Args:
            name (str):
                The name of the group that will be created.

        Returns:
            :obj:`dict`:
                The group resource record of the newly minted group.

        Examples:
            >>> group = tio.platform.groups.create('Group Name')
        '''
        return self._post(json={'name': name})

    def delete(self, id):
        '''
        Delete a user group.

        :devportal:`Endpoint Documentation <groups-delete>`

        Args:
            id (int): The unique identifier for the group to be deleted.

        Returns:
            :obj:`None`:
                The group was successfully deleted.

        Examples:
            >>> tio.platform.groups.delete(1)
        '''
        self._delete(id)

    def delete_user(self, group_id, user_id):
        '''
        Delete a user from a user group.

        :devportal:`Endpoint Documentation <groups-delete-user>`

        Args:
            group_id (int):
                The unique identifier for the group to be modified.
            user_id (int):
                The unique identifier for the user to be removed from the group.

        Returns:
            :obj:`None`:
                The user was successfully removed from the group.

        Examples:
            >>> tio.platform.groups.delete_user(1, 1)
        '''
        self.__delete('{}/users/{}'.format(group_id, user_id))

    def edit(self, id, name):
        '''
        Edit a user group.

        :devportal:`Endpoint Documentation <groups/edit>`

        Args:
            id (int):
                The unique identifier for the group to be modified.
            name (str):
                The new name for the group.

        Returns:
            :obj:`dict`:
                The group resource record.

        Examples:
            >>> tio.platform.groups.edit(1, 'Updated name')
        '''
        return self._put(id, json={'name': name})

    def list(self):
        '''
        Lists all of the available user groups.

        :devportal:`Endpoint Documentation <groups-list>`

        Returns:
            :obj:`list`:
                List of the group resource records

        Examples:
            >>> for group in tio.platform.groups.list():
            ...     pprint(group)
        '''
        return self._get().groups

    def list_users(self, id):
        '''
        List the user memberships within a specific user group.

        :devportal:`Endpoint Documentation <groups-list-users>`

        Args:
            id (int): The unique identifier of the group requested.

        Returns:
            :obj:`list`:
                List of user resource records based on membership to the
                specified group.

        Example:
            >>> for user in tio.platform.groups.list_users(1):
            ...     pprint(user)
        '''
        return self._get('{}/users'.format(id)).users
