from django.conf import settings

# File path json file is stored
SERVICE_ACCOUNT_KEY_FILE_PATH = getattr(settings, 'SERVICE_ACCOUNT_KEY_FILE_PATH', None)

# A key that is used for generating a custom token. This should be primary.
CUSTOM_TOKEN_KEY = getattr(settings, 'CUSTOM_TOKEN_KEY', 'id')
