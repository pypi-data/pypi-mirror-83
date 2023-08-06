import requests
from requests.exceptions import RequestException
from typing import Dict


def check_response(request_func):
    """ Verify the resquest response, checking for errors.

    Args:
        resp (Dict): The response

    Raises:
        BadRequest: Bad request, check your request
        Unauthorized: Invalid token
        Forbidden: You do not have permition to this resource.
        NotFound: Resource not found. Check the endpoint
        UnProcessableEntity: The server was unable to process the request
        UnknownServerError: Internal server error

    Returns:
        Dict: The response
    """
    def wrapper(*args, **kwargs):
        from timeit import default_timer as timer
        try:
            start = timer()
            resp = request_func(*args, **kwargs)
            end = timer()
            print(
                f'The request to ClickSign api lasted {(end - start):.3f} seconds'
            )
            print(f'{resp.headers}')
        except RequestException:
            raise

        if resp.status_code == 400:
            raise BadRequest(resp.text)
        elif resp.status_code == 401:
            raise Unauthorized(resp.text)
        elif resp.status_code == 403:
            raise Forbidden(resp.text)
        elif resp.status_code == 404:
            raise NotFound(resp.text)
        elif resp.status_code == 422:
            raise UnProcessableEntity(resp.text)
        elif resp.status_code == 429:
            raise TooManyRequests(resp.text, resp.headers)
        elif resp.status_code == 500:
            raise UnknownServerError(resp.text)
        return resp

    return wrapper


@check_response
def make_response(method, url, params, timeout, json=None):
    return requests.request(method=method,
                            url=url,
                            json=json,
                            params=params,
                            timeout=timeout)


class Forbidden(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return f'ClickSign API Error: Forbidden! Please verify if your token is valid and if you are in the right environment. The server response was: {self.error}.'


class Unauthorized(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return f'ClickSign API Error: Unauthorized! Invalid token. The server response was: {self.error}.'


class BadRequest(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return f'ClickSign API Error: BadRequest! The request you send is not valid. The server response was: {self.error}.'


class UnProcessableEntity(Exception):
    def __init__(self, error):
        self.message = error

    def __str__(self):
        return f'ClickSign API Error: UnProcessableEntity! The server was not able to process the request. The server response was: {self.message}.'


class NotFound(Exception):
    def __init__(self, error):
        self.message = error

    def __str__(self):
        return f'ClickSign API Error: NotFound! The server was not able to find this recurse. The server response was: {self.error}.'


class TooManyRequests(Exception):
    def __init__(self, error, headers):
        self.headers = headers
        self.error = error

    def __str__(self):
        return f'ClickSign API Error: TooManyRequests! You do reach the request rate limit! The server response was: {self.error}'


class UnknownServerError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return f'ClickSign API Error: UnknownServerError! The server was not able to process the request. Internal server error. The server response was: {self.error}.'
