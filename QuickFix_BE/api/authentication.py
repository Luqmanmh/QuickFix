from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom authentication class that reads the SimpleJWT token 
    directly out of HttpOnly secure cookies.
    """
    def authenticate(self, request):
        # Extract the token from cookies instead of headers
        raw_token = request.COOKIES.get('access_token')
        
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token