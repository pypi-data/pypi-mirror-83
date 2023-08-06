""" Script used to define the auth service"""

from vesicashapi.base import VesicashBase

class Auth(VesicashBase):
    """ docstring for Auth"""

    @classmethod
    def login(cls, **kwargs):
        """
        Log in a user
        Args:
            email_address: email address
            phone_number: phone number
            password: password
        Returns:
            Json data from Vesicash API.
        """

        return cls().requests.post('auth/login', data=kwargs)

    @classmethod
    def signup(cls, **kwargs):
        """
        Sign up a user
        Args:
            account_type: Account Type (individual, business)
            email_address: email address
            phone_number: phone number (optional)
            password: password (optional) 
            username: (optional)

        Returns:
            Json data from Vesicash API.
        """

        return cls().requests.post('auth/signup', data=kwargs)