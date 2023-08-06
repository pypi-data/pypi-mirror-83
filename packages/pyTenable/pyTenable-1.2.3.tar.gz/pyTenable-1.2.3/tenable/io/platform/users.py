'''
Users
=====

Methods described in this section relate to the the users API under the
platform section.  These methods can be accessed at
``TenableIO.platform.users``.

.. rst-class:: hide-signature
.. autoclass:: UsersAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from tenable.utils import dict_merge
from marshmallow import Schema, fields


class UserSchema(Schema):
    username = fields.Email()
    password = fields.String()
    permissions = fields.Integer()
    name = fields.Email()
    enabled = fields.Bool()
    type = fields.String(missing='local')


class UserCreateSchema(UserSchema):
    username = fields.Email(required=True)
    password = fields.String(required=True)
    permissions = fields.Integer(required=True)


class ChangePasswordSchema(Schema):
    password = fields.String(required=True)
    current_password = fields.String(required=True)


class UsersAPI(APIEndpoint):
    _path = 'users'

    def create(self, **kwargs):
        '''
        Create a new user.

        :devportal:`Endpoint documentation <users-create>`

        Args:
            username (str): The username for the new user.
            password (str): The password for the new user.
            permissions (int):
                The permissions role for the user.  The permissions integer
                is derived based on the desired role of the user.  For details
                describing what permissions values mean what roles, please refer
                to the `User Roles <https://cloud.tenable.com/api#/authorization>`_
                table to see what permissions are accepted.
            name (str, optional): The human-readable name of the user.
            email (str, optional): The email address of the user.
            type (str, optional):
                The account type for the user.  The default is `local`.

        Returns:
            :obj:`dict`:
                The resource record fo the new user.

        Examples:
            Create a standard user:

            >>> user = tio.platform.users.create(
            ...     username='jsmith@company.com',
            ...     password='password1',
            ...     permissions=32
            ... )

            Create an admin user and add the email and name:

            >>> user = tio.platform.create.users(
            ...     username='jdoe@company.com',
            ...     password='password',
            ...     permissions=64,
            ...     name='Jane Doe',
            ...     email='jdoe@company.com'
            ... )
        '''
        payload = UserCreateSchema().load(kwargs)
        return self._post(json=payload)

    def list(self):
        '''
        Returns a list of users.

        :devportal:`Endpoint documentation <users-list>`

        Returns:
            :obj:`list`:
                List of user resource objects.

        Examples:
            >>> for user in tio.platform.users.list():
            ...     print(user)
        '''
        return self._get().users

    def delete(self, id):
        '''
        Removes a user from Tenable.io.

        :devportal:`Endpoint documentation <users-delete>`

        Args:
            id (int): The unique identifier of the user.

        Returns:
            :obj:`None`:
                The user was successfully deleted.

        Examples:
            >>> tio.users.delete(1)
        '''
        return self._delete(id)

    def edit(self, id, **kwargs):
        '''
        Modify an existing user.

        :devportal:`Endpoint documentation <users-edit>`

        Args:
            id (int): The unique identifier for the user.
            permissions (int, optional):
                The permissions role for the user.  The permissions integer
                is derived based on the desired role of the user.  For details
                describing what permissions values mean what roles, please refer
                to the `User Roles <https://cloud.tenable.com/api#/authorization>`_
                table to see what permissions are accepted.
            name (str, optional): The human-readable name of the user.
            email (str, optional): The email address of the user.
            enabled (bool, optional): Is the user account enabled?

        Returns:
            :obj:`dict`:
                The modified user resource record.

        Examples:
            >>> user = tio.platform.users.edit(1, name='New Full Name')
        '''
        payload = UserSchema().load(dict_merge(self.details(id), kwargs))
        return self._put(json=payload)

    def enabled(self, id, status):
        '''
        Enable  or disable the user account.

        :devportal:`Endpoint documentation <users-enabled>`

        Args:
            id (int): The unique identifier for the user.
            enabled (bool): Is the user enabled?

        Returns:
            :obj:`dict`:
                The modified user resource record.

        Examples:
            Enable a user:

            >>> tio.platform.users.enabled(1, True)

            Disable a user:

            >>> tio.platform.users.enabled(1, False)
        '''
        return self._put('{}/enabled'.format(id),
            json={'enabled': bool(status)}
        )

    def change_password(self, id, **kwargs):
        '''
        Change the password for a specific user.

        :devportal:`Endpoint documentation <users-password>`

        Args:
            id (int): The unique identifier for the user.
            current_password (str): The current password.
            password (str): The new password.

        Returns:
            :obj:`None`:
                The password has been successfully changed.

        Examples:
            >>> tio.platform.users.change_password(1,
            ...     current_password='old_pass',
            ...     password='new_pass')
        '''
        payload = ChangePasswordSchema().load(kwargs)
        return self._put('{}/chpasswd'.format(id), json=payload)

    def gen_api_keys(self, id):
        '''
        Generate the API keys for a specific user.

        :devportal:`Endpoint documentation <user-keys>`

        Args:
            id (int): The unique identifier for the user.

        Returns:
            :obj:`dict`:
                A dictionary containing the new API Key-pair.

        Examples:
            >>> keys = tio.platform.users.gen_api_keys(1)
        '''
        return self._put('{}/keys'.format(id))

    # NOTE: The two-factor related APIs weren't added here.  Those APIs would
    #       need to be tested, and there wasn't much of any usage from outside
    #       the UI.  If there is demand for them from the community, they can
    #       be added back.
    #       * /users/{id}/two-factor/send-verification
    #       * /users/{id}/two-factor/verify-code
    #       * /users/{id}/two-factor