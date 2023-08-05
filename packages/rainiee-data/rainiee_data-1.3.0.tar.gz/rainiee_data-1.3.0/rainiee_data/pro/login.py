import json

import requests


class LoginApi:
    def __init__(self, username, password, timeout=15):
        self.__timeout = timeout
        self.__username = username
        self.__password = password
        self.__login_url = 'https://data.rainiee.com/api/v1.0/api-token-auth'

    def login(self):
        res = requests.get(self.__login_url, params={'username': self.__username, 'password': self.__password},
                           timeout=self.__timeout)
        result = json.loads(res.text)
        if result['code'] == 200:
            return result['data']
        raise Exception(result['message'])
