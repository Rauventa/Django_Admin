from rest_framework.authentication import TokenAuthentication as DefaultTokenAuthentication

from authtoken.models import Token


class TokenAuthentication(DefaultTokenAuthentication):
    model = Token
