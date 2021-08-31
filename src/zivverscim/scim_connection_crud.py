import urllib.parse

from .exceptions import ZivverMissingRequiredFields, ZivverCRUDError
from .external_connection import OauthConnection
from .wrapper import get_zivver_user_object


class ZivverSCIMConnection:
    """
    Object representing the zivver connection to do CRUD operations with
    """

    def __init__(self, external_oauth_token_value, scim_api_create_url, scim_api_update_url,
                 scim_api_get_url, scim_api_delete_url):
        self.external_oauth_token_value = external_oauth_token_value
        self.scim_api_create_url = scim_api_create_url
        self.scim_api_update_url = scim_api_update_url
        self.scim_api_get_url = scim_api_get_url
        self.scim_api_delete_url = scim_api_delete_url

    def _check_required_create_fields(self, last_name=None, user_name=None, sso_connection=None,
                               zivver_account_key=None):
        # Check for required fields
        if not self.external_oauth_token_value:
            raise ZivverMissingRequiredFields('Missing field: external_oauth_token_value')
        if not self.scim_api_create_url:
            raise ZivverMissingRequiredFields('Missing field: scim_api_create_url')
        if not self.scim_api_update_url:
            raise ZivverMissingRequiredFields('Missing field: scim_api_update_url')
        if not self.scim_api_get_url:
            raise ZivverMissingRequiredFields('Missing field: scim_api_get_url')
        if not self.scim_api_delete_url:
            raise ZivverMissingRequiredFields('Missing field: scim_api_delete_url')

        if not last_name:
            raise ZivverMissingRequiredFields('Missing field: last_name')
        if not user_name:
            raise ZivverMissingRequiredFields('Missing field: user_name')

        if sso_connection and not zivver_account_key:
            raise ZivverMissingRequiredFields('Missing field: zivver_account_key')

    def _check_required_delete_get_fields(self, account_id):
        """
        Checks if the account ID is empty
        :param account_id:
        :except If the required account_id is empty
        """
        if not account_id:
            raise ZivverMissingRequiredFields('Missing field: account_id')

    def _check_response(self, response):
        """
        Check the repsone for errors, raise if there are any errors.
        """
        if type(response) is not dict and response.status_code in [400, 401, 403, 404]:
            raise ZivverCRUDError(message='Response from Zivver with Errors', response=response)

    def create_user_in_zivver(self, first_name=None, last_name=None, nick_name=None, user_name=None,
                              zivver_account_key=None, sso_connection=False, is_active=False, aliases=[],
                              delegates=[]):
        """
        Create a user in Zivver via SCIM.
        :return: Returns the ZivverUser() object
        """
        self._check_required_create_fields(last_name=last_name, user_name=user_name, sso_connection=sso_connection,
                                           zivver_account_key=zivver_account_key)

        # Set defaults
        if not first_name:
            first_name = ''

        scim_object_user = {
            'schemas': [
                'urn:ietf:params:scim:schemas:core:2.0:User',
                'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User',
                'urn:ietf:params:scim:schemas:zivver:0.1:User'
            ],
            'meta': {
                'resourceType': 'User'
            },
            'active': is_active,
            'name': {
                'formatted': '{} {}'.format(first_name, last_name)
            },
            'nickName': nick_name,
            'urn:ietf:params:scim:schemas:zivver:0.1:User': {
                'SsoAccountKey': zivver_account_key,
                'aliases': aliases,
                'delegates': delegates
            },
            'userName': user_name
        }

        oauth_connection = OauthConnection(external_oauth_token_value=self.external_oauth_token_value)
        response = oauth_connection.return_request_post_data(post_url=self.scim_api_create_url,
                                                             object_serialized=scim_object_user)

        self._check_response(response)

        zivver_user = get_zivver_user_object(response)
        return zivver_user

    def delete_user_from_zivver(self, account_id):
        """
        Delete the user from Zivver.
        NOTE: Deleting the user is irreversible
        :return: Returns the response object
        """
        self._check_required_delete_get_fields(account_id)

        oauth_connection = OauthConnection(external_oauth_token_value=self.external_oauth_token_value)
        delete_url = urllib.parse.urljoin(self.scim_api_delete_url, account_id)
        response = oauth_connection.return_request_delete_data(delete_url=delete_url)

        self._check_response(response)

        return response

    def get_user_from_zivver(self, account_id):
        """
        Returns the user from Zivver if the user exists
        :param account_id:
        :return: ZivverUser() object
        """
        self._check_required_delete_get_fields(account_id)

        oauth_connection = OauthConnection(external_oauth_token_value=self.external_oauth_token_value)
        get_url = urllib.parse.urljoin(self.scim_api_get_url, account_id)
        response = oauth_connection.return_request_get_data(get_url=get_url)

        self._check_response(response)

        zivver_user = get_zivver_user_object(response)
        return zivver_user

    def get_all_users_from_zivver(self):
        """
        Returns a list of users from Zivver
        :param account_id:
        :return: List(ZivverUser()) object
        """
        oauth_connection = OauthConnection(external_oauth_token_value=self.external_oauth_token_value)
        response = oauth_connection.return_request_get_data(get_url=self.scim_api_get_url)

        self._check_response(response)

        zivver_users = []
        for zivver_scim_user in response['Resources']:
            zivver_users.append(get_zivver_user_object(zivver_scim_user))

        return zivver_users

    def update_user_in_zivver(self, account_id, first_name=None, last_name=None, nick_name=None, user_name=None,
                              zivver_account_key=None, sso_connection=False, is_active=False, aliases=[],
                              delegates=[]):
        """
        Update a user in Zivver via SCIM.
        :return: Returns the ZivverUser() object
        """
        self._check_required_create_fields(last_name=last_name, user_name=user_name, sso_connection=sso_connection,
                                           zivver_account_key=zivver_account_key)

        self._check_required_delete_get_fields(account_id)

        # Set defaults
        if not first_name:
            first_name = ''

        scim_object_user = {
            'schemas': [
                'urn:ietf:params:scim:schemas:core:2.0:User',
                'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User',
                'urn:ietf:params:scim:schemas:zivver:0.1:User'
            ],
            'meta': {
                'resourceType': 'User',
                'location': '/scim/v2/Users/{}'.format(account_id)
            },
            'active': is_active,
            'id': account_id,
            'name': {
                'formatted': '{} {}'.format(first_name, last_name)
            },
            'nickName': nick_name,
            'urn:ietf:params:scim:schemas:zivver:0.1:User': {
                'SsoAccountKey': zivver_account_key,
                'aliases': aliases,
                'delegates': delegates
            },
            'userName': user_name
        }

        oauth_connection = OauthConnection(external_oauth_token_value=self.external_oauth_token_value)
        put_url = urllib.parse.urljoin(self.scim_api_update_url, account_id)
        response = oauth_connection.return_request_put_data(put_url=put_url, object_serialized=scim_object_user)

        self._check_response(response)

        zivver_user = get_zivver_user_object(response)
        return zivver_user
