import falcon
import urlparse
import httplib
import requests
from utils import (to_base_10, to_base_62, validate_url, build_url,
    get_base_hostname)
from models import UrlMap


class UrlShortenerHandler(object):
    def on_get(self, req, resp, shortened_url):
        if not shortened_url:
            raise falcon.HTTPBadRequest(
                'No shortened URL provided'
            )
        url_query = UrlMap.select().where(
                UrlMap.id == to_base_10(shortened_url)
            )
        if not url_query.exists():
            raise falcon.HTTPBadRequest(
                'Invalid shortened URL'
            )
        url_obj = url_query[0]
        url = url_obj.url
        resp.status = falcon.HTTP_301
        resp.location = url

    def on_post(self, req, resp):
        if 'url' not in req.json:
            raise falcon.HTTPBadRequest(
                'No url key provided in body'
            )
        url = req.json['url']
        if not validate_url(url):
            raise falcon.HTTPBadRequest(
                'Invalid URL'
            )
        shortend_url = get_base_hostname()
        url_query = UrlMap.select().where(UrlMap.url == url)
        url_obj = {}
        if not url_query.exists():
            url_obj = UrlMap.create(url=url)
        else:
            url_obj = url_query[0]
        shortend_url += '/' + to_base_62(url_obj.id)
        resp.body = {
            'shortened_url': shortend_url
        }
        resp.status = falcon.HTTP_201
