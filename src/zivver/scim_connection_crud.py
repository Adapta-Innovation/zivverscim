from .exceptions import ZivverMissingRequiredFields
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

    def _check_required_fields(self, last_name=None, nick_name=None, user_name=None, sso_connection=None,
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
        if not nick_name:
            raise ZivverMissingRequiredFields('Missing field: nick_name')
        if not user_name:
            raise ZivverMissingRequiredFields('Missing field: user_name')

        if sso_connection and not zivver_account_key:
            raise ZivverMissingRequiredFields('Missing field: zivver_account_key')

    def create_user_in_zivver(self, first_name=None, last_name=None, nick_name=None, user_name=None,
                              zivver_account_key=None, sso_connection=False, schemas=None, is_active=False):
        """
        Create a user in Zivver via SCIM.
        :return: Returns the ZivverUser() object
        """
        self._check_required_fields(last_name=last_name, nick_name=nick_name, user_name=user_name,
                                    sso_connection=sso_connection, zivver_account_key=zivver_account_key)

        # Set defaults
        if not first_name:
            first_name = ''
        if not schemas:
            schemas = [
                          'urn:ietf:params:scim:schemas:core:2.0:User',
                          'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User',
                          'urn:ietf:params:scim:schemas:zivver:0.1:User'
                      ],

        scim_object_user = {
            'schemas': schemas,
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
            },
            'userName': user_name
        }

        oauth_connection = OauthConnection(external_oauth_token_value=self.external_oauth_token_value)
        result = oauth_connection.return_request_post_data(post_url=self.scim_api_create_url,
                                                           object_serialized=scim_object_user)

        zivver_user = get_zivver_user_object(result)
        return zivver_user
