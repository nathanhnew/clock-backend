import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import Account


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        '''
        This methid is called on every request regardless
        of whether the endpoint needs authentication or not

        'authenticate' has 2 possible return values:

        'None' = if do not wish to authenticate. I.E. authentication
                 will fail (lack of token in header etc)
        '(user, token)' = return user/token combo when auth is
                            successful.

                            if neither met and an error, return nothing.
                            simply raise "AuthenticationFailed" '''

        request.user = None

        # 'auth_header' should be an array with 2 elements.
        # Name of authentication header (i.e. 'token') and
        # JWT that should authenticate against
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            # Invalid token header. no credentials provided
            return None
        elif len(auth_header) > 2:
            # Invalid token header. Should not contain spaces
            return None

        # The JWT library cant handle 'byte' types. To get around
        # we decode the prefix and token
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            # Unexpected header prefix
            return None

        # Now we know there is a chance authentication will succeed
        # Delegate actual authenticaton to a new method
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        '''
        Try to authenticate the given credentials. if successful,
        REturn token and user. If not error
        '''
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Invalid authentication. Could not decode token'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = Account.objects.get(pk=payload['id'])
        except Account.DoesNotExist:
            msg = 'No user matching this token was found'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = "This account has been deactivated"
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)
