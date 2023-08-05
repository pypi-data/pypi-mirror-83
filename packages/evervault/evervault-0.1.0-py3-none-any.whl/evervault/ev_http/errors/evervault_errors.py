class EvervaultError(Exception):

    def __init__(self, message=None, context=None):
        super(EvervaultError, self).__init__(message)
        self.message = message
        self.context = context


class ArgumentError(ValueError, EvervaultError):
    pass


class HttpError(EvervaultError):
    pass


class ResourceNotFound(EvervaultError):
    pass


class AuthenticationError(EvervaultError):
    pass


class ServerError(EvervaultError):
    pass


class BadGatewayError(EvervaultError):
    pass


class ServiceUnavailableError(EvervaultError):
    pass


class BadRequestError(EvervaultError):
    pass


class RateLimitExceeded(EvervaultError):
    pass


class ResourceNotRestorable(EvervaultError):
    pass


class MultipleMatchingUsersError(EvervaultError):
    pass


class UnexpectedError(EvervaultError):
    pass


class TokenUnauthorizedError(EvervaultError):
    pass


class TokenNotFoundError(EvervaultError):
    pass


error_codes = {
  'unauthorized': AuthenticationError,
  'forbidden': AuthenticationError,
  'bad_request': BadRequestError,
  'action_forbidden': BadRequestError,
  'missing_parameter': BadRequestError,
  'parameter_invalid': BadRequestError,
  'parameter_not_found': BadRequestError,
  'client_error': BadRequestError,
  'type_mismatch': BadRequestError,
  'not_found': ResourceNotFound,
  'admin_not_found': ResourceNotFound,
  'not_restorable': ResourceNotRestorable,
  'rate_limit_exceeded': RateLimitExceeded,
  'service_unavailable': ServiceUnavailableError,
  'server_error': ServiceUnavailableError,
  'conflict': MultipleMatchingUsersError,
  'unique_user_constraint': MultipleMatchingUsersError,
  'token_unauthorized': TokenUnauthorizedError,
  'token_not_found': TokenNotFoundError,
  'token_revoked': TokenNotFoundError,
  'token_blocked': TokenNotFoundError,
  'token_expired': TokenNotFoundError
}
