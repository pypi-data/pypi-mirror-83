import firebase_admin
from firebase_admin import credentials

from .app_settings import SERVICE_ACCOUNT_KEY_FILE_PATH

if SERVICE_ACCOUNT_KEY_FILE_PATH is not None:
	cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_FILE_PATH)
	firebase_admin = firebase_admin.initialize_app(cred)
else:
	firebase_admin = firebase_admin.initialize_app()
