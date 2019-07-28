
from google.oauth2 import id_token
from google.auth.transport import requests


CLIENT_ID = "973869074920-ues0cr8vkhg6shh08cvkc9o40mtaeg8k.apps.googleusercontent.com"


class tokenIDHlpeer:
    """
    this class handles the Google Authentication for the server
    """
    @staticmethod
    def tokenParser(token):
        """
        this function receives a token and returns some information of the user - after authentication
        :param token: user's token id
        :return: tuple of user id and user name
        """
        try:
            id_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            user_id = id_info['sub']
            user_name = 'no_name'
            if 'name' in id_info:
                user_name = id_info['name']
            return user_id, user_name
        except ValueError:
                # Invalid token
                pass
