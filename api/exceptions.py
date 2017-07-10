from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


class SettingsDoesNotExist(APIException):
    status_code = 400
    default_detail = 'The requested settings do not exist'


def _handle_generic_error(exc, context, response):
    # Define a custom error handler.
    # Take the response and wrap in 'errors' key
    response.data = {
        'errors': response.data
    }

    return response


def core_exception_handler(exc, context):
    # If an exception is thrown that we don't explicity explain,
    # We want delegation to default
    response = exception_handler(exc, context)
    handlers = {
        'ValidationError': _handle_generic_error,
        'SettingsDoesNotExist': _handle_generic_error
    }
    # This is how we identify the exception.
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        # If exception is one we can handle, then we will.
        # Otherwise return the standard response
        return handlers[exception_class](exc, context, response)

    return response
