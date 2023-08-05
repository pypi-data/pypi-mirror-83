
from datetime import datetime
from errors import error_handler

import certifi
import json
import logging
import os
import requests

logger = logging.getLogger('evervault.request')

class Request(object):

    def __init__(self):
        self.http_session = requests.Session()
        self.timeout = 5000

    def make_request(self, url, method, auth, params=None):
        """ Construct an API request, send it to the API, and parse the
        response. """
        from evervault import __version__

        req_params = self._build_headers(method, params, __version__)

        # request logging
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Sending %s request to: %s", method, url)
            logger.debug("  headers: %s", req_params.headers)
            if method == 'GET':
                logger.debug("  params: %s", req_params['params'])
            else:
                logger.debug("  params: %s", req_params['data'])

        if self.http_session is None:
            resp = requests.request(
                    method, url, timeout=self.timeout,
                    auth=auth, verify=certifi.where(), **req_params)
        else:
            resp = self.http_session.request(
                    method, url, timeout=self.timeout,
                    auth=auth, verify=certifi.where(), **req_params)

        # response logging
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Response received from %s", url)
            logger.debug("  encoding=%s status:%s",
                                                                    resp.encoding, resp.status_code)
            logger.debug("  content:\n%s", resp.content)

        parsed_body = self.parse_body(resp)
        error_handler.raise_errors_on_failure(resp)
        return parsed_body

    def _build_headers(self, method, params, version):
        req_params = {}
        headers = {
                        'User-Agent': 'evervault-python/' + version,
                        'AcceptEncoding': 'gzip, deflate',
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
        }
        if method in ('POST', 'PUT', 'DELETE'):
            req_params['data'] = json.dumps(params, cls=json.JSONEncoder)
        elif method == 'GET':
            req_params['params'] = params
        req_params['headers'] = headers
        return req_params

    def parse_body(self, resp):
        if resp.content and resp.content.strip():
            try:
                # use supplied or inferred encoding to decode the
                # response content
                decoded_body = resp.content.decode(
                        resp.encoding or resp.apparent_encoding)
                body = json.loads(decoded_body)
                if body.get('type') == 'error.list':
                    error_handler.raise_application_errors_on_failure(body, resp.status_code)  # noqa
                return body
            except ValueError:
                error_handler.raise_errors_on_failure(resp)
