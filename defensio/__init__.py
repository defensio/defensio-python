import urllib
import httplib
import json

API_VERSION = '2.0'
API_HOST    = 'api.defensio.com'
LIB_VERSION = '0.9'
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
    """ GETs user info for this api_key """
    return self._call('GET', self._generate_url_path())

  def post_document(self, data):
    """ POSTs a new document to defensio
    data -- A dictionary representing the new document
    """
    return self._call('POST', self._generate_url_path('document'), data)

  def get_document(self, signature):
    """ GETs the Defensio result for a document
    signature -- The signature of the desired document
    """
    return self._call('GET', self._generate_url_path('document', signature))

  def put_document(self, signature, data):
    """ PUTs (Changes the status) of an existing defensio document
    signature -- The signature for the desired document
    data      -- A dictionary with the new allowed value eg. {'allow': false}
    """
    return self._call('PUT', self._generate_url_path('document', signature), data)

  def get_basic_stats(self):
    """ GETs Basic usage/accuracy stats """
    return self._call('GET', self._generate_url_path('basic-stats'))

  def get_extended_stats(self, data):
    """ GETs Extended usage/accuracy stats 
    data -- A dictionary with the range of dates you want the stats for {'from': '2010/01/01', 'to': '2010/01/10'}
    """
    return self._call('GET', self._generate_url_path('extended-stats'))

  def post_profanity_filter(self, data):
    """ POSTs data that will be filtered by a predefined dictionary.
        data -- Fields to be filtered
    """
    return self._call('POST', self._generate_url_path('profanity-filter'), data)

  def handle_post_document_async_callback(self, request):
    self._parse_body(str(request))

  def _call(self, method, path, data=None):
    conn = httplib.HTTPConnection(API_HOST)

    if data:
      headers = {'Content-type': 'application/x-www-form-urlencoded'}
      conn.request(method, path, urllib.urlencode(data), headers)

    else:
      conn.request(method, path)

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
    return json.loads(body)

def handle_post_document_async_callback(request):
  """ Shortcut function to handle callbacks """
  Defensio(None).handle_post_document_async_callback(request)
