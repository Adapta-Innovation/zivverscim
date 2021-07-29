import os
from dotenv import load_dotenv

load_dotenv()


class ZivverConfig:
    """
    Zivver configuration for testing Zivver CRUD
    """
    zivver_test_domain = os.getenv('ZIVVER_TEST_DOMAIN', 'zivver.com')
    zivver_test_api_key = os.getenv('ZIVVER_TEST_API_KEY', None)
    zivver_test_endpoint_url = os.getenv('ZIVVER_TEST_ENDPOINT_URL', 'https://app.zivver.com/api/scim/v2/Users/')
