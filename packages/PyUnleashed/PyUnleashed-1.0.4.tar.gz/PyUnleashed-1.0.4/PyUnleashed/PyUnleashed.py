# -*- coding: utf-8 -*-

"""
Unleashed Software API Class
"""

__title__ = "PyUnleashed"
__version__ = "1.0.4"
__author__ = "John Horton"
__license__ = "MIT"

from requests import request
import hashlib
import hmac
import base64
import datetime
import json
from urllib.parse import urlencode

class API(object):
    """ API Class """

    def __init__(self, url, api_id, api_key, **kwargs):
        self.url = url
        self.api_id = api_id
        self.api_key = api_key
        self.timeout = kwargs.get("timeout", 5)

    @property
    def api_key_bytes(self):
        """ create bytes of api_key """
        return self.api_key.encode('utf-8')

    def get_url(self, endpoint, **kwargs):
        """ generate URL for requests """
        url = self.url
        if url.endswith("/") is False:
            url = "{0}/".format(url)
        queryString = urlencode(kwargs)
        return "{0}{1}?{2}".format(url, endpoint, queryString)

    def encodeQuery(self, **kwargs):
        """ encode query and hash string """
        queryString = urlencode(kwargs)
        queryStringBytes = queryString.encode('utf-8')
        api_id_bytes = self.api_key_bytes
        hash = hmac.new(api_id_bytes, msg=queryStringBytes, digestmod=hashlib.sha256).digest()
        hash64 = base64.b64encode(hash).decode()
        return hash64

    def getHeaders(self, **kwargs):
        """ generate headers """
        headers = {
            'Accept': 'application/json',
            'api-auth-id': self.api_id,
            'api-auth-signature': self.encodeQuery(**kwargs),
            'Content-Type': 'application/json'
        }
        return headers

    def request(self, method=None, endpoint=None, data=None, params=None, **kwargs):
            """ make requests """
            url = self.get_url(endpoint, **kwargs)

            if params is None:
                params = {}

            encoded_params = urlencode(params)

            headers = self.getHeaders(**kwargs)

            if data is not None:
                data = json.dumps(data, ensure_ascii=False).encode('utf-8')

            return request(
                method=method,
                url=url,
                params=params,
                data=data,
                timeout=self.timeout,
                headers=headers
            )

    def get(self, endpoint, **kwargs):
        """ Get requests """
        return self.request("GET", endpoint, None, **kwargs)

    def post(self, endpoint, data, **kwargs):
        """ POST requests """
        return self.request("POST", endpoint, data, **kwargs)

    def put(self, endpoint, data, **kwargs):
        """ PUT requests """
        return self.request("PUT", endpoint, data, **kwargs)

    def delete(self, endpoint, **kwargs):
        """ DELETE requests """
        return self.request("DELETE", endpoint, None, **kwargs)

    @staticmethod
    def dateFromUnl(unl_datetime):
        """ convert date from UNL to datetime """
        return datetime.datetime.utcfromtimestamp(int(''.join(filter(str.isdigit, unl_datetime))) / 1000).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def dateToUnl(datetime_unl=None):
        """ convert date from datetime to UNL """
        if datetime_unl:
            return datetime.datetime.timestamp(datetime_unl)
        else:
            return datetime.datetime.timestamp(datetime.datetime.now())
