import re  # regular expressions
from urlparse import urlparse
from urlparse import urlunparse

from constants import StatusCode
from constants import UrlTypes
import requests


def get_requests_header(url):
    head = None
    try:
        head = requests.head(url, allow_redirects=True)
    except Exception:
        # bad requests exception
        pass
    return head


def get_redirect_url(head):
    return head.url


def get_url_response_code(head):
    status_code = None
    if head is None:
        status_code = StatusCode.BAD_REQUEST
    status_code = head.status_code
    return status_code


def get_error(status_code):
    if status_code == StatusCode.BAD_REQUEST:
        return StatusCode.BAD_REQUEST, StatusCode.get_status_message(StatusCode.BAD_REQUEST)
    if status_code == StatusCode.UNAUTHORIZED:
        return StatusCode.UNAUTHORIZED, StatusCode.get_status_message(StatusCode.UNAUTHORIZED)
    if status_code == StatusCode.FORBIDDEN:
        return StatusCode.FORBIDDEN, StatusCode.get_status_message(StatusCode.FORBIDDEN)
    if status_code == StatusCode.NOT_FOUND:
        return StatusCode.NOT_FOUND, StatusCode.get_status_message(StatusCode.NOT_FOUND)
    if status_code == StatusCode.INTERNAL_SERVER_ERROR:
        return StatusCode.INTERNAL_SERVER_ERROR, StatusCode.get_status_message(StatusCode.INTERNAL_SERVER_ERROR)
    return StatusCode.OK, None


def sanitize_url(url):
    parsed_url = urlparse(url)
    if not re.match('(http|https)', parsed_url.scheme):
        url = 'http://' + url
        parsed_url = urlparse(url)

    return parsed_url.geturl()


def remove_url_fragments(url):
    scheme, netloc, path, params, query, fragment = urlparse(url)
    parsed_url = urlunparse((scheme, netloc, path, params, query, ""))
    return parsed_url


def remove_url_queries(url):
    scheme, netloc, path, params, query, fragment = urlparse(url)
    parsed_url = urlunparse((scheme, netloc, path, params, "", fragment))
    return parsed_url


def get_domain_url(url):
    parsed_uri = urlparse(url)
    provider_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return provider_url


def get_url_type(url, status_code):
    parsed_url = urlparse(url)
    netloc_url = parsed_url.netloc
    error_code, error_msg = get_error(status_code)
    if error_code != StatusCode.OK:
        return UrlTypes.ERROR
    if UrlTypes.get_special_url(UrlTypes.DOCS) in netloc_url:
        return UrlTypes.DOCS
    if UrlTypes.get_special_url(UrlTypes.DROPBOX) in netloc_url:
        return UrlTypes.DROPBOX
    if UrlTypes.get_special_url(UrlTypes.WIKI) in netloc_url:
        return UrlTypes.WIKI
    if UrlTypes.get_special_url(UrlTypes.YOUTUBE) in netloc_url:
        return UrlTypes.YOUTUBE
    return UrlTypes.GENERAL
