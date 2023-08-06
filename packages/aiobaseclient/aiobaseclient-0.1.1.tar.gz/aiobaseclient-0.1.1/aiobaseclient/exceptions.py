from izihawa_utils.exceptions import BaseError


class ClientError(BaseError):
    code = 'client_error'


class WrongContentTypeError(ClientError):
    code = 'wrong_content_type_error'


class ExternalServiceError(ClientError):
    code = 'external_service_error'

    def __init__(self, url, status_code, text):
        self.info = {
            'url': url,
            'status_code': status_code,
            'text': text,
        }


class TemporaryError(BaseError):
    code = 'temporary_error'


class NotFoundError(BaseError):
    code = 'not_found_error'


class MethodNotAllowedError(BaseError):
    code = 'method_not_allowed_error'


class ServiceUnavailableError(TemporaryError):
    code = 'service_unavailable_error'


class TooManyRequestsError(TemporaryError):
    code = 'too_many_requests_error'
