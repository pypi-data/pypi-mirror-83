from . import evervault_errors as errors


def raise_errors_on_failure(resp):
    if resp.status_code == 404:
        raise errors.ResourceNotFound('Resource Not Found')
    elif resp.status_code == 401:
        raise errors.AuthenticationError('Unauthorized')
    elif resp.status_code == 403:
        raise errors.AuthenticationError('Forbidden')
    elif resp.status_code == 500:
        raise errors.ServerError('Server Error')
    elif resp.status_code == 502:
        raise errors.BadGatewayError('Bad Gateway Error')
    elif resp.status_code == 503:
        raise errors.ServiceUnavailableError('Service Unavailable')

def raise_application_errors_on_failure(error_list_details, http_code):
    error_details = error_list_details['errors'][0]
    error_code = error_details.get('type')
    if error_code is None:
        error_code = error_details.get('code')
    error_context = {
      'http_code': http_code,
      'application_error_code': error_code
    }
    error_class = errors.error_codes.get(error_code)
    if error_class is None:
        # unexpected error
        if error_code:
            message = message_for_unexpected_error_with_type(error_details, http_code)
        else:
            message = message_for_unexpected_error_without_type(error_details, http_code)
        error_class = errors.UnexpectedError
    else:
        message = error_details.get('message')
    raise error_class(message, error_context)

def message_for_unexpected_error_with_type(error_details, http_code):  # noqa
    error_type = error_details.get('type')
    message = error_details.get('message')
    return "The error of type '%s' is not recognized. It occurred with the message: %s and http_code: '%s'. Please contact Intercom with these details." % (error_type, message, http_code)  # noqa

def message_for_unexpected_error_without_type(error_details, http_code):  # noqa
    message = error_details['message']
    return "An unexpected error occured. It occurred with the message: %s and http_code: '%s'. Please contact Intercom with these details." % (message, http_code)  # noqa
