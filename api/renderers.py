import json
from rest_framework.renderers import JSONRenderer


class APIJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'

    def render(self, data, media_type=None, renderer_context=None):
        # If view throws error (authentication, etc.). 'data' will contain
        # an errors key. Want default JSON renderer to handle errors
        errors = data.get('errors', None)

        if errors is not None:
            return super(APIJSONRenderer, self).render(data)

        # Now we can render data to the defined namespace
        return json.dumps({
            self.object_label: data
        })


class AccountJSONRenderer(APIJSONRenderer):
    object_label = 'account'

    def render(self, data, media_type=None, renderer_context=None):

        # If we receive a 'token' in a response, it will be a byte
        # object which doesnt serialize well. Need to decode first
        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        return super(AccountJSONRenderer, self).render(data)


class SettingsJSONRenderer(APIJSONRenderer):
    object_label = 'settings'
