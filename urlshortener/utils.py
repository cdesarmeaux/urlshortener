import string
import math
import urlparse
import os

base = string.digits + string.lowercase + string.uppercase


def to_base_62(val):
    new_base = 62
    result = []
    while val > 0:
        n = int(val % new_base)
        result.append(base[n])
        val = math.floor(val/new_base)
    return ''.join(result[::-1])


def to_base_10(val):
    result = 0
    old_base = 62
    for n in xrange(len(val)):
        result = old_base * result + base.find(val[n])
    return result


def validate_url(url):
    try:
        url_parts = urlparse.urlparse(urlparse.urljoin(url, '/'))
        parts_valid = all([url_parts.scheme, url_parts.netloc, url_parts.path])
        netloc_valid = len(url_parts.netloc.replace('www.', '').split('.')) > 1
        return parts_valid and netloc_valid
    except:
        return False


def build_url(hostname, scheme='http', port=None, path=None):
    netloc = ':'.join((hostname, str(port))) if port else hostname
    full = '/'.join((netloc, path)) if path else netloc
    url = '://'.join((scheme, full))
    return url


def get_base_hostname():
    result = 'localhost'
    try:
        result = os.environ['HOST']
    except:
        pass
    try:
        result = ':'.join((result, str(os.environ['PORT'])))
    except:
        pass
    return result