import sys

def is_python3():
  return sys.version_info[0] == 3

if is_python3():
  import urllib.parse
  import http.client
else:
  import urllib
  import httplib

import json

API_VERSION = '2.0'
API_HOST    = 'api.defensio.com'
LIB_VERSION = '0.9.1'
ROOT_NODE   = 'defensio-result'
FORMAT      = 'json'
USER_AGENT  = "Defensio-Python %(LIB_VERSION)s"%locals()
CLIENT      = "Defensio-Python | %(LIB_VERSION)s | Camilo Lopez | clopez@websense.com"%locals()

class Defensio(object):
  """Small, but full featured Defensio client class"""

  def __init__(self, api_key, client=CLIENT):
    """Constructor
    api_key -- A defensio api key you can get one from http://defensio.com/
    client -- Client siganture for your application for details see http://defensio.com/api 
    """
    self.client = client
    self.api_key = api_key

  def get_user(self):
    """ Get information about the api key """
    return self._call('GET', self._generate_url_path())

  def post_document(self, data):
    """
    Create and analyze a new document
    data -- A Dictionary representing the new document
    """
    data.update({ 'client' : CLIENT })
    return self._call('POST', self._generate_url_path('documents'), data)

  def get_document(self, signature):
    """ 
    Get the status of an existing document
    signature -- The signature of the desired document
    """
    return self._call('GET', self._generate_url_path('documents', signature))

  def put_document(self, signature, data):
    """ 
    Modify the properties of an existing document
    signature -- The signature for the desired document
    data      -- A Dictionary with the new allowed value eg. {'allow': false}
    """
    return self._call('PUT', self._generate_url_path('documents', signature), data)

  def get_basic_stats(self):
    """ Get basic statistics for the current user """
    return self._call('GET', self._generate_url_path('basic-stats'))

  def get_extended_stats(self, data):
    """ 
    Get more exhaustive statistics for the current user
    data -- A dictionary with the range of dates you want the stats for {'from': '2010/01/01', 'to': '2010/01/10'}
    """
    return self._call('GET', self._generate_url_path('extended-stats') + '?' + self._urlencode(data))

  def post_profanity_filter(self, data):
    """ 
    Filter a set of values based on a pre-defined dictionary
    data -- Fields to be filtered
    """
    return self._call('POST', self._generate_url_path('profanity-filter'), data)

  def handle_post_document_async_callback(self, request):
    """
    Takes the request string of an async request callback and returns a Dictionary
    request -- String posted by Defensio as a callback
    """
    return self._parse_body(request)

  def _call(self, method, path, data=None):
    """ Do the actual HTTP request """
    if is_python3():
      conn = http.client.HTTPConnection(API_HOST)
    else:
      conn = httplib.HTTPConnection(API_HOST)

    headers = {'User-Agent' : USER_AGENT}

    if data:
      headers.update( {'Content-type': 'application/x-www-form-urlencoded'} )
      conn.request(method, path, self._urlencode(data), headers)

    else:
      conn.request(method, path, None, headers)

    response = conn.getresponse()
    result   =  [response.status, self._parse_body(response.read())]
    conn.close()
    return result

  def _generate_url_path(self, action=None, id=None):
    url = '/' + API_VERSION + '/users/' + self.api_key
    if action: url = url + '/' + action
    if id:     url = url + '/' + id
    url = url + '.' + FORMAT
    return url

  def _parse_body(self, body):
    """ For just call a deserializer for FORMAT"""
    if is_python3():
      return json.loads(body.decode('UTF-8'))
    else:
      return json.loads(body)

  def _urlencode(self, url):
      if is_python3():
        return urllib.parse.urlencode(url)
      else:
        return urllib.urlencode(url)


def handle_post_document_async_callback(request):
  """ Shortcut function to handle callbacks """
  Defensio(None).handle_post_document_async_callback(request)
