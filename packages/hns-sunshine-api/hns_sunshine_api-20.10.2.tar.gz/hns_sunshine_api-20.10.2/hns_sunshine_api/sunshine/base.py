import requests

from requests.adapters import HTTPAdapter


class HTTPtimeoutAdapter(HTTPAdapter):
    """ Adds timeout to requests HTTP adapter """

    def __init__(self, timeout: int = 5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = timeout

    def send(self, *args, **kwargs):
        if kwargs.get('timeout') is None:
            kwargs['timeout'] = self.timeout
        return super(HTTPtimeoutAdapter, self).send(*args, **kwargs)


class SunshineBase:
    _OBJECTS_ROOT = 'api/sunshine/objects'

    _RELATIONSHIPS_ROOT = 'api/sunshine/relationships'

    _PROFILES_ROOT = 'api/v2/user_profiles'

    _EVENTS_ROOT = 'api/v2/user_profiles'

    _USERS_ROOT = 'api/v2/users'

    _HEADERS = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self, subdomain: str, email: str, key: str, global_timeout: int = 5):
        """
        Creates and manages objects on zendesk sunshine

        :param subdomain: Your zendesk subdomain
        :param email: Sunshine user email ID. Used for token based authentication
        :param key: Sunshine token.
        :param global_timeout: Request timeout in seconds for every request within the session
        """

        self.subdomain = subdomain
        self._objects_base_url = f'https://{self.subdomain}.zendesk.com/{self._OBJECTS_ROOT}'
        self._relationships_base_url = f'https://{self.subdomain}.zendesk.com/{self._RELATIONSHIPS_ROOT}'
        self._profiles_base_url = f'https://{self.subdomain}.zendesk.com/{self._PROFILES_ROOT}'
        self._events_base_url = f'https://{self.subdomain}.zendesk.com/{self._EVENTS_ROOT}'
        self._users_base_url = f'https://{self.subdomain}.zendesk.com/{self._USERS_ROOT}'

        self._session = requests.Session()

        self._adapter = HTTPtimeoutAdapter(global_timeout)
        self._session.mount('http://', self._adapter)
        self._session.mount('https://', self._adapter)

        self._session.headers.update(self._HEADERS)

        self._session.auth = (f'{email}/token', f'{key}')

    def __repr__(self):
        return f'{self.__class__.__name__}(subdomain="{self.subdomain}")'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def close_session(self):
        """ Closes requests session """

        self._session.close()
