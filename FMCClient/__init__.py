import requests
from requests.auth import HTTPBasicAuth
import urllib3
from datetime import datetime, timedelta


class FMCError(Exception):
    pass


class FMCAuthError(Exception):
    pass


class Client:
    def __init__(self, verify=bool(), warnings=bool(), api_version='v1'):
        self.verify = bool(verify)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) if warnings is False else None

        self.api_version = api_version
        self.headers = {'Content-Type': 'application/json'}
        self.server = None
        self.token = None
        self.token_refresh = None
        self.uuid = None
        self.base_url = None
        self.token_expire = datetime.now()
        self.token_refresh_count = 0

    def connect(self, server=str(), username=str(), password=str()):
        self.server = server
        url = ('https://{}/api/fmc_platform/v1/auth/generatetoken'.format(server))
        _response = requests.post(url, headers=self.headers, auth=HTTPBasicAuth(username, password), verify=self.verify)

        if _response.status_code in [204]:
            token = _response.headers.get('X-auth-access-token')
            uuid = _response.headers.get('DOMAIN_UUID')
            self.token_refresh = _response.headers.get('X-auth-refresh-token')
            self.token = token
            self.uuid = uuid
            self.token_expire = datetime.now() + timedelta(minutes=30)
            self.token_refresh_count = 0
            self.base_url = 'https://{}/api/fmc_config/{}/domain/{}'.format(server, self.api_version, uuid)
            self.headers.update({'X-auth-access-token': token})
            return _response.status_code
        elif _response.status_code == 401:
            raise FMCAuthError('Authentication Error!')
        else:
            raise FMCError('HTTP Error,  Status Code: {}'.format(_response.status_code))

    def validate_token(self):
        if self.token_refresh_count >= 3:
            raise FMCAuthError('Token cannot be refresh! New token is required.')
        elif self.token_expire <= datetime.now():
            self.refresh_token_func()
        else:
            return True

    def refresh_token_func(self):
        url = ('https://{}/api/fmc_platform/v1/auth/refreshtoken'.format(self.server))
        headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.token,
                   'X-auth-refresh-token': self.token_refresh}
        _response = requests.post(url, headers=headers, verify=self.verify)

        if _response.status_code in [204]:
            token = _response.headers.get('X-auth-access-token')
            uuid = _response.headers.get('DOMAIN_UUID')
            self.token_refresh = _response.headers.get('X-auth-refresh-token')
            self.token = token
            self.uuid = uuid
            self.token_expire = datetime.now() + timedelta(minutes=30)
            self.token_refresh_count = self.token_refresh_count + 1
            self.base_url = 'https://{}/api/fmc_config/{}/domain/{}'.format(self.server,
                                                                            self.api_version,
                                                                            uuid)
            self.headers.update({'X-auth-access-token': token})
            return _response.status_code
        elif _response.status_code == 401:
            raise FMCAuthError('Authentication Error!')
        else:
            raise FMCError('HTTP Error,  Status Code: {}'.format(_response.status_code))

    def close(self):
        url = ('https://{}/api/fmc_platform/v1/auth/revokeaccess'.format(self.server))
        __response = requests.post(url, headers=self.headers, verify=False)
        return __response.status_code

    def get(self, method=str(), **kwargs):
        response = requests.get('{}/{}'.format(self.base_url.strip('/'), method), headers=self.headers,
                                verify=self.verify, params=kwargs)
        if response.status_code in [200]:
            return response.json()
        else:
            raise FMCError(response.status_code)

    def update(self, method: str, data: dict) -> dict:
        response = requests.put('{}/{}'.format(self.base_url.strip('/'), method), headers=self.headers,
                                verify=self.verify, json=data)
        if response.status_code in [200]:
            return response.json()
        else:
            raise FMCError(response.status_code)
