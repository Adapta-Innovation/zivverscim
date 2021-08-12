import json


def get_zivver_user_object(zivver_scim):
    """
    Wrapper to wrap Zivver SCIM to Zivver Python Class
    :param zivver_scim: Returned from the Zivver response, contains the object on create/update
    :return: Zivver()
    """    
    account_id = zivver_scim.get('id', '')

    name_formatted = zivver_scim.get('name', '')
    if name_formatted:
        name_formatted = name_formatted.get('formatted', '')

    meta = zivver_scim.get('meta', '')
    meta_created_at = ''
    meta_location = ''
    meta_resource_type = ''
    if meta:
        meta_created_at = meta.get('created', '')
        meta_location = meta.get('location', '')
        meta_resource_type = meta.get('resourceType', '')
        
    phone_numbers = zivver_scim.get('phoneNumbers', [])
    
    user_name = zivver_scim.get('userName', '')
    nick_name = zivver_scim.get('nickName', '')
    is_active = zivver_scim.get('active', False)

    schemas = zivver_scim.get('schemas', [])
    enterprise_user = zivver_scim.get('urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', '')
    
    zivver_scim_user = zivver_scim.get('urn:ietf:params:scim:schemas:zivver:0.1:User', '')
    zivver_scim_user_aliases = ''
    zivver_scim_user_delegates = ''
    if zivver_scim_user:
        zivver_scim_user_aliases = zivver_scim_user.get('aliases', [])
        zivver_scim_user_delegates = zivver_scim_user.get('delegates', [])
    
    return ZivverUser(account_id=account_id, name_formatted=name_formatted, meta_location=meta_location,
                      meta_created_at=meta_created_at, meta_resource_type=meta_resource_type,
                      phone_numbers=phone_numbers, user_name=user_name, nick_name=nick_name, is_active=is_active,
                      schemas=schemas, enterprise_user=enterprise_user,
                      zivver_scim_user_aliases=zivver_scim_user_aliases,
                      zivver_scim_user_delegates=zivver_scim_user_delegates)


class ZivverUser:
    """
    ZivverUser Class object created from the ZivverUser create/update response
    """

    def __init__(self, account_id=None, name_formatted=None, meta_created_at=None, meta_location=None,
                 meta_resource_type=None, phone_numbers=None, user_name=None, nick_name=None, is_active=False,
                 schemas=None, enterprise_user=None, zivver_scim_user_aliases=None, zivver_scim_user_delegates=None):
        self.account_id = account_id
        self.name_formatted = name_formatted
        self.meta_created_at = meta_created_at
        self.meta_location = meta_location
        self.meta_resource_type = meta_resource_type
        self.phone_numbers = phone_numbers
        self.user_name = user_name
        self.nick_name = nick_name
        self.is_active = is_active
        self.schemas = schemas
        self.enterprise_user = enterprise_user
        self.zivver_scim_user_aliases = zivver_scim_user_aliases
        self.zivver_scim_user_delegates = zivver_scim_user_delegates

    def __str__(self):
        """
        Representation of the SCIM user response in JSON
        :return: SCIM Response json object
        """
        return json.dumps(
            {
                'id': self.account_id,
                'name': {
                    'formatted': self.name_formatted
                },
                'meta': {
                    'created': self.meta_created_at,
                    'location': self.meta_location,
                    'resourceType': self.meta_resource_type
                },
                'phoneNumbers': self.phone_numbers,
                'schemas': self.schemas,
                'userName': self.user_name,
                'nickName': self.nick_name,
                'active': self.is_active,
                'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User': self.enterprise_user,
                'urn:ietf:params:scim:schemas:zivver:0.1:User': {
                    'aliases': self.zivver_scim_user_aliases,
                    'delegates': self.zivver_scim_user_delegates
                }
            }, indent=4
        )
