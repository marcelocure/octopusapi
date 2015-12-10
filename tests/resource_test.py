import unittest
from octopusapi import Resource, Field, OctopusApp
import config
import falcon
import requests
import thread
import time


def start_api():
	fields = []
	fields.append(Field(name='serialNumber', type='string', description='Device serial number'))
	fields.append(Field(name='activationLocation', type='string', description='Activation Location'))

	def get(request, response):
	    response.body = 'get received'
	    response.status = falcon.HTTP_200

	def put(request, response):
	    response.body = 'put received'
	    response.status = falcon.HTTP_200

	order = Resource('order', fields, get=get, put=put)

	app = OctopusApp('test', [order], config)
	app.run_server()

thread.start_new_thread(start_api, () )

class Test(unittest.TestCase):
	def test_should_return_200_get(self):
		response = requests.get('http://127.0.0.1:8000/test/order')
		self.assertEqual(response.status_code, 200)

	def test_should_return_200_put(self):
		response = requests.put('http://127.0.0.1:8000/test/order')
		self.assertEqual(response.status_code, 200)

	def test_should_return_404(self):
		response = requests.get('http://127.0.0.1:8000/test/order2')
		self.assertEqual(response.status_code, 404)

	def test_should_return_405(self):
		response = requests.delete('http://127.0.0.1:8000/test/order')
		self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()