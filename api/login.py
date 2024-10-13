import json
import requests
import settings
from utils.extract_token import extract_token


class UserLogin:

    def __init__(self):
        self.base_url = 'https://api.dev.abra-market.com/'

    def user_login(self, email=None, password=None) -> json:
        """Sends a request to the site's Swagger API to log in the user using a predefined email and password,
        retrieving the access token from the response"""

        email = email or settings.SUPPLIER_EMAIL
        password = password or settings.PASSWORD

        data = {'email': email, 'password': password}
        headers = {'Content-Type': 'application/json'}
        res = requests.post(self.base_url + 'auth/sign-in', data=json.dumps(data), headers=headers)
        status = res.status_code
        body = res.json()
        cookies = res.headers.get('Set-Cookie')
        if status == 200:
            access_token = extract_token(cookies, 'access_token_cookie')
            return access_token, status, body
        else:
            return None, status, body

    def user_logout(self, email=None, password=None):
        """Sends a request to the site's Swagger API to log out the user by invalidating the access token"""

        access_token, _, _ = self.user_login(email, password)
        headers = {'Content-Type': 'application/json',
                   'Cookie': f'access_token_cookie={access_token}'}
        res = requests.delete(self.base_url + 'auth/sign-out', headers=headers)
        status = res.status_code
        body = res.json()
        return status, body


# login = UserLogin()
# login.user_login()
# login.user_logout()
