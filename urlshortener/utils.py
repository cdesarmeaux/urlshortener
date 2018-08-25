import string
import math
import urlparse

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
        result = urlparse.urlparse(url)
        if result.path:
            return all([result.scheme, result.netloc, result.path])
        return all([result.scheme, result.netloc])
    except:
        return False


def build_url(hostname, scheme='http', port=None, path=None):
    netloc = ':'.join((hostname, str(port))) if port else hostname
    full = '/'.join((netloc, path)) if path else netloc
    url = '://'.join((scheme, full))
    return url
