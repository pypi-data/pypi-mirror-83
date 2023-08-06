import os

from django.conf import global_settings
from configurations import Configuration, values


def getvalue(key):
    return getattr(global_settings, key, None)


class BaseConfiguration(Configuration):
    BASE_DIR = os.getcwd()
    ROOT_URLCONF = values.Value(None)
    SITE_ID = values.IntegerValue(None)

    # CORE
    DEBUG = values.BooleanValue(default=getvalue('DEBUG'))
    DEBUG_PROPAGATE_EXCEPTIONS = values.BooleanValue(
        default=getvalue('DEBUG_PROPAGATE_EXCEPTIONS'))
    INTERNAL_IPS = values.ListValue(default=getvalue('INTERNAL_IPS'))
    ALLOWED_HOSTS = values.ListValue(default=getvalue('ALLOWED_HOSTS'))
    TIME_ZONE = values.Value(default=getvalue('TIME_ZONE'))
    USE_TZ = values.Value(default=getvalue('USE_TZ'))
    LANGUAGE_CODE = values.Value(default=getvalue('LANGUAGE_CODE'))
    LANGUAGES_BIDI = values.Value(default=getvalue('LANGUAGES_BIDI'))
    USE_I18N = values.Value(default=getvalue('USE_I18N'))
    LOCALE_PATHS = values.ListValue(default=getvalue('LOCALE_PATHS'))
    USE_L10N = values.Value(default=getvalue('USE_L10N'))
    DEFAULT_CHARSET = values.Value(default=getvalue('DEFAULT_CHARSET'))
    SERVER_EMAIL = values.Value(default=getvalue('SERVER_EMAIL'))
    DATABASE_ROUTERS = values.Value(default=getvalue('DATABASE_ROUTERS'))
    EMAIL_BACKEND = values.Value(default=getvalue('EMAIL_BACKEND'))
    EMAIL_HOST = values.Value(default=getvalue('EMAIL_HOST'))
    EMAIL_PORT = values.IntegerValue(default=getvalue('EMAIL_PORT'))

    INSTALLED_APPS = values.ListValue(default=getvalue('INSTALLED_APPS'))
    FORM_RENDERER = values.Value(default=getvalue('FORM_RENDERER'))
    DISALLOWED_USER_AGENTS = values.Value(
        default=getvalue('DISALLOWED_USER_AGENTS'))
    IGNORABLE_404_URLS = values.Value(default=getvalue('IGNORABLE_404_URLS'))
    SECRET_KEY = values.SecretValue()
    DEFAULT_FILE_STORAGE = values.Value(
        default=getvalue('DEFAULT_FILE_STORAGE'))
    MEDIA_ROOT = values.Value(default=getvalue('MEDIA_ROOT'))
    MEDIA_URL = values.Value(default=getvalue('MEDIA_URL'))
    STATIC_ROOT = values.Value(default=getvalue('STATIC_ROOT'))
    STATIC_URL = values.Value(default=getvalue('STATIC_URL'))
    FILE_UPLOAD_HANDLERS = values.ListValue(
        default=getvalue('FILE_UPLOAD_HANDLERS'))
    FILE_UPLOAD_MAX_MEMORY_SIZE = values.IntegerValue(
        default=getvalue('FILE_UPLOAD_MAX_MEMORY_SIZE'))
    DATA_UPLOAD_MAX_MEMORY_SIZE = values.IntegerValue(
        default=getvalue('DATA_UPLOAD_MAX_MEMORY_SIZE'))
    DATA_UPLOAD_MAX_NUMBER_FIELDS = values.IntegerValue(
        default=getvalue('DATA_UPLOAD_MAX_NUMBER_FIELDS'))
    FILE_UPLOAD_TEMP_DIR = values.Value(
        default=getvalue('FILE_UPLOAD_TEMP_DIR'))

    STATICFILES_DIRS = values.ListValue(default=getvalue('STATICFILES_DIRS'))

    WSGI_APPLICATION = values.Value(default=getvalue('WSGI_APPLICATION'))

    # MIDDLEWARE
    MIDDLEWARE = values.ListValue(default=getvalue('MIDDLEWARE'))

    # AUTHENTICATION
    AUTH_USER_MODEL = values.Value(default=getvalue('AUTH_USER_MODEL'))
    AUTHENTICATION_BACKENDS = values.ListValue(
        default=getvalue('AUTHENTICATION_BACKENDS'))
    LOGIN_URL = values.Value(default=getvalue('LOGIN_URL'))
    LOGIN_REDIRECT_URL = values.Value(default=getvalue('LOGIN_REDIRECT_URL'))
    LOGOUT_REDIRECT_URL = values.Value(default=getvalue('LOGOUT_REDIRECT_URL'))
    PASSWORD_RESET_TIMEOUT_DAYS = values.IntegerValue(
        default=getvalue('PASSWORD_RESET_TIMEOUT_DAYS'))
    PASSWORD_RESET_TIMEOUT = values.IntegerValue(
        default=getvalue('PASSWORD_RESET_TIMEOUT'))
    PASSWORD_HASHERS = values.ListValue(default=getvalue('PASSWORD_HASHERS'))
    AUTH_PASSWORD_VALIDATORS = values.ListValue(
        default=getvalue('AUTH_PASSWORD_VALIDATORS'))

    # SIGNING
    SIGNING_BACKEND = values.Value(default=getvalue('SIGNING_BACKEND'))

    # CSRF
    CSRF_FAILURE_VIEW = values.Value(default=getvalue('CSRF_FAILURE_VIEW'))
    CSRF_COOKIE_NAME = values.Value(default=getvalue('CSRF_COOKIE_NAME'))
    CSRF_COOKIE_AGE = values.IntegerValue(default=getvalue('CSRF_COOKIE_AGE'))
    CSRF_COOKIE_DOMAIN = values.Value(default=getvalue('CSRF_COOKIE_DOMAIN'))
    CSRF_COOKIE_PATH = values.Value(default=getvalue('CSRF_COOKIE_PATH'))
    CSRF_COOKIE_SECURE = values.BooleanValue(
        default=getvalue('CSRF_COOKIE_SECURE'))
    CSRF_COOKIE_HTTPONLY = values.BooleanValue(
        default=getvalue('CSRF_COOKIE_HTTPONLY'))
    CSRF_COOKIE_SAMESITE = values.Value(
        default=getvalue('CSRF_COOKIE_SAMESITE'))
    CSRF_HEADER_NAME = values.Value(default=getvalue('CSRF_HEADER_NAME'))
    CSRF_TRUSTED_ORIGINS = values.ListValue(
        default=getvalue('CSRF_TRUSTED_ORIGINS'))
    CSRF_USE_SESSIONS = values.BooleanValue(
        default=getvalue('CSRF_USE_SESSIONS'))

    # MESSAGES
    MESSAGE_STORAGE = values.Value(default=getvalue('MESSAGE_STORAGE'))

    # LOGGING
    LOGGING_CONFIG = values.Value(default=getvalue('LOGGING_CONFIG'))
    DEFAULT_EXCEPTION_REPORTER = values.Value(
        default=getvalue('DEFAULT_EXCEPTION_REPORTER'))
    DEFAULT_EXCEPTION_REPORTER_FILTER = values.Value(
        default=getvalue('DEFAULT_EXCEPTION_REPORTER_FILTER'))

    # TESTING
    TEST_RUNNER = values.Value(default=getvalue('TEST_RUNNER'))
    TEST_NON_SERIALIZED_APPS = values.ListValue(
        default=getvalue('TEST_NON_SERIALIZED_APPS'))

    # FIXTURES
    FIXTURE_DIRS = values.ListValue(default=getvalue('FIXTURE_DIRS'))

    # STATICFILES
    STATICFILES_DIRS = values.ListValue(default=getvalue('STATICFILES_DIRS'))
    STATICFILES_STORAGE = values.Value(default=getvalue('STATICFILES_STORAGE'))
    STATICFILES_FINDERS = values.ListValue(
        default=getvalue('STATICFILES_FINDERS'))

    # SYSTEM CHECKS
    SILENCED_SYSTEM_CHECKS = values.ListValue(
        default=getvalue('SILENCED_SYSTEM_CHECKS'))

    # SECURITY MIDDLEWARE
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(
        default=getvalue('SECURE_BROWSER_XSS_FILTER'))
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(
        default=getvalue('SECURE_CONTENT_TYPE_NOSNIFF'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(
        default=getvalue('SECURE_HSTS_INCLUDE_SUBDOMAINS'))
    SECURE_HSTS_PRELOAD = values.BooleanValue(
        default=getvalue('SECURE_HSTS_PRELOAD'))
    SECURE_HSTS_SECONDS = values.IntegerValue(
        default=getvalue('SECURE_HSTS_SECONDS'))
    SECURE_REDIRECT_EXEMPT = values.ListValue(
        default=getvalue('SECURE_REDIRECT_EXEMPT'))
    SECURE_REFERRER_POLICY = values.Value(
        default=getvalue('SECURE_REFERRER_POLICY'))
    SECURE_SSL_HOST = values.Value(default=getvalue('SECURE_SSL_HOST'))
    SECURE_SSL_REDIRECT = values.BooleanValue(
        default=getvalue('SECURE_SSL_REDIRECT'))

    @classmethod
    def pre_setup(cls):
        super(BaseConfiguration, cls).pre_setup()
        if cls.DEBUG:
            cls.ALLOWED_HOSTS = ['*']


"""
https://github.com/django/django/blob/master/django/conf/global_settings.py
"""
