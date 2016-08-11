
""" Interface to the Gerrit REST API. """
import os
import sys
import json
import logging
import requests
import ConfigParser
import platform
from requests.auth import HTTPDigestAuth

GERRIT_MAGIC_JSON_PREFIX = ")]}\'\n"
GERRIT_AUTH_SUFFIX = "/a"


def check_authentication(response):
    content = response.content.strip()
    http_error_msg = ''
    if response.status_code == 403 or response.status_code == 400:

        if content == u'Authentication required' or content == u'Not Signed In':
            http_error_msg = u'You need to be authrised to do this.Please set your username and password' \
                             u' in ~/.grtrc.'
        elif content == u'Forbidden' or content == u'sdfsd':
            http_error_msg = u'Your password or username is wrong.'
    elif response.status_code == 401:
        http_error_msg = u'This is caused by wrong password or username ,or you are not authorzed'
    elif 400 <= response.status_code < 500:
        http_error_msg = 'other failure:%s' % response.status_code
    elif 500 <= response.status_code < 600:
        http_error_msg = 'other failure:%s' % response.status_code

    if http_error_msg:
        print 'From server:%s' % content
        print http_error_msg
        exit(0)


def _decode_response(response):
    """ Strip off Gerrit's magic prefix and decode a response.

    :returns:
        Decoded JSON content as a dict, or raw text if content could not be
        decoded as JSON.

    :raises:
        requests.HTTPError if the response contains an HTTP error status code.

    """
    content = response.content.strip()
    logging.debug(content[:512])
    check_authentication(response)
#   response.raise_for_status()
    if content.startswith(GERRIT_MAGIC_JSON_PREFIX):
        content = content[len(GERRIT_MAGIC_JSON_PREFIX):]
    try:
        return json.loads(content)
    except ValueError:
        logging.error('Invalid json content: %s' % content)
        raise


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class GerritRestAPI(Singleton):

    """ Interface to the Gerrit REST API.

    :arg str url: The full URL to the server, including the `http(s)://` prefix.
        If `auth` is given, `url` will be automatically adjusted to include
        Gerrit's authentication suffix.
    :arg auth: (optional) Authentication handler.  Must be derived from
        `requests.auth.AuthBase`.
    :arg boolean verify: (optional) Set to False to disable verification of
        SSL certificates.

    """

    def __init__(self, url=None, auth=None, verify=True):

        cf = ConfigParser.ConfigParser()
        if platform.system() == 'Windows':
            home = os.environ['HOMEPATH']
        else:
            home = os.environ['HOME']
        cf.read(home + "/.grtrc")

        if cf.has_option("grt", "url") and cf.get("grt", "url") != u'':
            cf_url = cf.get("grt", "url")
        else:
            sys.stderr.write("The url of server hasn't been configured,please configure \"url\" in %s/.grtrc\n Or run 'gerrit_config'" % home)
            exit(0)

        if cf.has_option("grt", "username") and cf.has_option("grt", "password"):
            if cf.get("grt", "username") != u'' and cf.get("grt", "password") != u'':
                cf_username = cf.get("grt", "username")
                cf_password = cf.get("grt", "password")
                auth = HTTPDigestAuth(cf_username, cf_password)

        headers = {'Accept': 'application/json',
                   'Accept-Encoding': 'gzip'}
        self.kwargs = {'auth': auth,
                       'verify': verify,
                       'headers': headers}
        self.url = str(cf_url).rstrip('/')

        if auth:
            if not isinstance(auth, requests.auth.AuthBase):
                raise ValueError('Invalid auth type; must be derived '
                                 'from requests.auth.AuthBase')

            if not self.url.endswith(GERRIT_AUTH_SUFFIX):
                self.url += GERRIT_AUTH_SUFFIX
        else:
            if self.url.endswith(GERRIT_AUTH_SUFFIX):
                self.url = self.url[: - len(GERRIT_AUTH_SUFFIX)]

        if not self.url.endswith('/'):
            self.url += '/'
        logging.debug("url %s", self.url)

    def make_url(self, endpoint):
        """ Make the full url for the endpoint.

        :arg str endpoint: The endpoint.

        :returns:
            The full url.

        """

        endpoint = endpoint.lstrip('/')
        return self.url + endpoint

    def get(self, endpoint, **kwargs):
        """ Send HTTP GET to the endpoint.

        :arg str endpoint: The endpoint to send to.

        :returns:
            JSON decoded result.

        :raises:
            requests.RequestException on timeout or connection error.

        """
        kwargs.update(self.kwargs.copy())
        response = requests.get(self.make_url(endpoint), **kwargs)
        return _decode_response(response)

    def put(self, endpoint, **kwargs):
        """ Send HTTP PUT to the endpoint.

        :arg str endpoint: The endpoint to send to.

        :returns:
            JSON decoded result.

        :raises:
            requests.RequestException on timeout or connection error.

        """
        kwargs.update(self.kwargs.copy())
        if "data" in kwargs:
            kwargs["headers"].update(
                {"Content-Type": "application/json;charset=UTF-8"})
        response = requests.put(self.make_url(endpoint), **kwargs)
        return _decode_response(response)

    def post(self, endpoint, **kwargs):
        """ Send HTTP POST to the endpoint.

        :arg str endpoint: The endpoint to send to.

        :returns:
            JSON decoded result.

        :raises:
            requests.RequestException on timeout or connection error.

        """
        kwargs.update(self.kwargs.copy())
        if "data" in kwargs:
            kwargs["headers"].update(
                {"Content-Type": "application/json;charset=UTF-8"})
        response = requests.post(self.make_url(endpoint), **kwargs)

        return _decode_response(response)

    def delete(self, endpoint, **kwargs):
        """ Send HTTP DELETE to the endpoint.

        :arg str endpoint: The endpoint to send to.

        :returns:
            JSON decoded result.

        :raises:
            requests.RequestException on timeout or connection error.

        """
        kwargs.update(self.kwargs.copy())
        response = requests.delete(self.make_url(endpoint), **kwargs)
        return _decode_response(response)
