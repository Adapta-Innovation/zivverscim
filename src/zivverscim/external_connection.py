import json
import requests


class OauthConnection:
    """
    Object will be post/update/delete via this class in the external application
    """

    def __init__(self, external_oauth_token_value=None, extra_headers=None):
        self.external_oauth_token_value = external_oauth_token_value
        self.custom_oauth_header = {
            'header_key': 'Authorization',
            'header_value': 'Bearer {}'.format(self.external_oauth_token_value)
        }
        self.extra_headers = extra_headers

    def add_extra_headers(self, extra_headers):
        """
        Add extra headers to the OAuth object
        """
        self.extra_headers = extra_headers

    def set_custom_oauth_authorization_header(self, header_key, header_value):
        """
        Update the oauth Authorization header with your own key/value
        Default is:
        { 'Authorization': 'Bearer [token]',
        ...
        }
        """
        self.custom_oauth_header = {
            'header_key': header_key,
            'header_value': header_value
        }

    def _get_content_length_of_object_serialized(self, object_serialized):
        """
        Returns the length of the serialized object
        """
        content_length = len(json.dumps(object_serialized))
        return content_length

    def _create_authorization_header(self, object_serialized=None):
        """
        Creates the headers that are send with the requests
        """
        header_key = self.custom_oauth_header['header_key']
        header_value = self.custom_oauth_header['header_value']

        headers = {
            header_key: header_value,
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

        # add extra headers if any:
        if self.extra_headers:
            for key, val in self.extra_headers.items():
                headers[key] = val

        if object_serialized is not None:
            content_length = self._get_content_length_of_object_serialized(object_serialized)
            headers['Content-Length'] = '{}'.format(content_length)

        return headers

    def return_request_post_data(self, post_url, object_serialized):
        """
        Do a POST request to the URL
        :return: The defualt json() object, if none, then returns the response object
        """
        headers = self._create_authorization_header(object_serialized)
        result = requests.post(post_url, headers=headers, json=object_serialized)
        try:
            return result.json()
        except Exception:
            return result

    def return_request_get_data(self, get_url):
        """
        Do a GET request to the url and return the data
        :return: The defualt json() object, if none, then returns the response object
        """
        headers = self._create_authorization_header()
        result = requests.get(get_url, headers=headers)
        try:
            return result.json()
        except Exception:
            return result

    def return_request_delete_data(self, delete_url):
        """
        Requests a DELETE method
        :return: The defualt json() object, if none, then returns the response object
        """
        headers = self._create_authorization_header()
        result = requests.delete(delete_url, headers=headers)
        try:
            return result.json()
        except Exception:
            return result

    def return_request_patch_data(self, patch_url, object_serialized):
        """
        Do a PATCH request to the URL
        :return: The defualt json() object, if none, then returns the response object
        """
        headers = self._create_authorization_header(object_serialized)
        result = requests.patch(patch_url, headers=headers, json=object_serialized)
        try:
            return result.json()
        except Exception:
            return result

    def return_request_put_data(self, put_url, object_serialized):
        """
        Do a PUT request to the URL
        :return: The defualt json() object, if none, then returns the response object
        """
        headers = self._create_authorization_header(object_serialized)
        result = requests.put(put_url, headers=headers, json=object_serialized)
        try:
            return result.json()
        except Exception:
            return result
