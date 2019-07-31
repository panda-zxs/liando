import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# liando/etc/settings/wisdom_brain.py
ROOT_DIR = environ.Path(__file__) - 3
env = environ.Env()
NAME_ID_LENGTH = 6
VERSION = 'v1.0'
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/users/login"
LOGOUT_URL = "/users/logout"