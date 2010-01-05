import unittest
import sys
sys.path.append('.')
from defensio import *


class TestDefensio(unittest.TestCase):

  def setUp(self):
    # Set this to an actual key before running tests
    self.api_key  = 'key'
    self.client = Defensio(self.api_key)

  def testGenerateUrls(self):
    self.assertEqual('/2.0/users/key.json', self.client._generate_url_path())
    self.assertEqual('/2.0/users/key/action1.json', self.client._generate_url_path('action1'))
    self.assertEqual('/2.0/users/key/action1/id1.json', self.client._generate_url_path('action1', 'id1'))

  def testGetUser(self):
    status, result =  self.client.get_user()
    self.assertEqual(200, status)
    self.assertEqual(dict, type(result['defensio-result']))
    result_body = result['defensio-result']
    self.assertEqual('success', result_body['status'])
    self.assertEqual('',        result_body['message'])
    self.assertEqual('2.0',     result_body['api-version'])

    self.assertEqual(unicode, type(result_body['owner-url']))
    self.assertTrue(len(result_body['owner-url']) > 0 )

  def testPostDocumentWhenFail(self):
    doc = {'content': 'Hi Hola Salut'}
    status, result = self.client.post_document(doc)
    self.assertEqual(200, status)
    self.assertEqual(dict, type(result['defensio-result']))
    result_body = result['defensio-result']
    self.assertEqual('fail', result_body['status'])
    self.assertEqual('The following fields are missing but required: platform, type', result_body['message'])
    self.assertEqual('2.0', str(result_body['api-version']))

  def testPostDocumentWhenSuccessThenPutThenGet(self):
    doc = {'content': 'Hi Hola Salut', 'type' : 'comment', 'platform' : 'python-test'}
    status, result = self.client.post_document(doc)
    self.assertEqual(200, status)
    self.assertEqual(dict, type(result['defensio-result']))

    result_body = result['defensio-result']
    self.assertEqual('success', result_body['status'])
    self.assertEqual('', result_body['message'])
    self.assertEqual('2.0', str(result_body['api-version']))
    self.assertAlmostEqual(0.05, result_body['spaminess'])
    self.assertEqual('legitimate', result_body['classification'])
    self.assertEqual(None, result_body['profanity-match'])
    self.assertTrue(result_body['allow'])

    self.assertEqual(unicode, type( result_body['signature'] ))

    signature = result_body['signature']

    status, put_result = self.client.put_document(signature, {'allow' : 'false'})
    self.assertEqual(200, status)
    put_result_body = put_result['defensio-result']
    self.assertEqual('success', put_result_body['status'])

    status, get_result = self.client.get_document(signature)
    self.assertFalse(get_result['defensio-result']['allow'])

  def testProfanityFilter(self):
    doc = {'bad' : 'some fucking cursing here', 'good' : 'Hey... how is it going?'}
    status, res = self.client.post_profanity_filter(doc)
    self.assertEqual(200, status)
    self.assertEqual('Hey... how is it going?', res['defensio-result']['good'])
    self.assertEqual('some ***ing cursing here', res['defensio-result']['bad'])

if __name__ == '__main__':
  unittest.main()