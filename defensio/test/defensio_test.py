import unittest
import sys
sys.path.append('.')
from defensio import *


class TestDefensio(unittest.TestCase):

  def setUp(self):
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

if __name__ == '__main__':
  unittest.main()
