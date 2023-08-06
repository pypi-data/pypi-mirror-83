'''
Session
=======

Methods described in this section relate to the the session API under the
platform section.  These methods can be accessed at
``TenableIO.platform.session``.

.. rst-class:: hide-signature
.. autoclass:: SessionAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from tenable.utils import check
from marshmallow import Schema, fields
from .users import ChangePasswordSchema
from restfly.errors import UnauthorizedError, base_msg_func as msg_func


class UpdateUserSchema(Schema):
    name = fields.String()
    email = fields.Email()


class SessionAPI(APIEndpoint):
    _path = 'session'

    def session(self):
        '''
        Retrieves the current user's session details.

        :devportal:`Endpoint documentation <session-get>`

        Returns:
            :obj:`dict`:
                The Session Details.

        Examples:
            >>> s = tio.platform.session.session()
        '''
        return self._get()

    def update(self, **kwargs):
        '''
        Updates the current user's attributes.

        :devportal:`Endpoint documentation <session-edit>`

        Args:
            name (str, optional):
                The new name for the user.
            email (str, optional):
                The new email address for the user.

        Returns:
            :obj:`dict`:
                The updates session details.

        Examples:
            >>> tio.platform.session.update(name='John Doe')
        '''
        payload = UpdateUserSchema().load(kwargs)
        return self._put(json=payload)

    def impersonate(self, username=None, user_id=None):
        '''
        Impersonates the specified user.

        :devportal:`Endpoint Documentation <users-impersonate>`

        Args:
            username (str, optional):
                The username to impersonate.  Usernames are required for API Key
                authenticated sessions.
            user_id (int, optional):
                The numeric id for the user to impersonate.  User ids are
                required for session-based authenticated sessions.

        Examples:
            >>> tio.platform.session.impersonate(username='joe@company.com')
        '''
        if self._api._auth_mech == 'user':
            if check('user_id', user_id, int, allow_none=False):
                self._api.post('users/{}/impersonate'.format(user_id))
        elif self._api._auth_mech == 'keys':
            if check('username', username, str, allow_none=False):
                self._api_session.headers.update({
                    'X-Impersonate': 'username={}'.format(username)
                })
        else:
            raise UnauthorizedError('Unauthenticated session', func=msg_func)

    def unimpersonate(self):
        '''
        Restores an impersonation to the original user.

        :devportal:`Endpoint Documentation <session-restore>`

        Examples:
            >>> tio.platform.session.unimpersonate()
        '''
        if self._api._auth_mech == 'user':
            self._post('restore')
        elif self._api._auth_mech == 'keys':
            self._api_session.headers.update({
                'X-Impersonate': None
            })
        else:
            raise UnauthorizedError('Unauthenticated session', func=msg_func)

    def change_password(self, current, new):
        '''
        Updates the password for the currently authenticated user.

        :devportal:`Endpoint Documentation <session-password>`

        Args:
            current_password (str): The current password.
            password (str): The new password.

        Returns:
            :obj:`None`:
                The password has been successfully changed.

        Examples:
            >>> tio.platform.session.change_password(
            ...     current_password='old_pass',
            ...     password='new_pass')
        '''
        payload = ChangePasswordSchema().load(kwargs)
        return self._put('chpasswd', json=payload)

    def keys(self):
        '''
        Generates new API Keys for the currently authenticates user.  Note that
        this will also update the API keys stored within the library as well.

        :devportal:`Endpoint Documentation <session-keys>`

        Returns:
            :obj:`dict`:
                The updated keys.

        Examples:
            >>> keys = tio.platform.session.keys()
        '''
        keys = self._put('keys', box_attrs={'camel_killer_box': True})

        # If the session was using session-based authentication previously, we
        # will want to log the user out of the API first before re-authing with
        # the API keys.
        if self._api._auth_mech == 'user':
            self._api._deauthenticate()

        # Re-auth with the new keys and then return the API Keys.
        self._api._authenticate(
            access_key=keys.access_key,
            secret_key=keys.secret_key
        )
        return keys

    # NOTE: The two-factor related APIs weren't added here.  Those APIs would
    #       need to be tested, and there wasn't much of any usage from outside
    #       the UI.  If there is demand for them from the community, they can
    #       be added back.
    #       * /session/two-factor/send-verification
    #       * /session/two-factor/verify-code
    #       * /session/two-factor