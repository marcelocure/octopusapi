from octopusapi import Resource, Field, OctopusApp
import config
import falcon


fields = []
fields.append(Field(name='serialNumber', type='string', description='Device serial number'))
fields.append(Field(name='status', type='string', description='Order status', valid_values=['processing', 'error', 'completed']))
fields.append(Field(name='activationLocation', type='string', description='Activation Location'))

def get(request, response):
	print request
	response.body = 'fuck yeahhh!!'
	response.status = falcon.HTTP_200

def post(request, response):
	print request
	response.status = falcon.HTTP_200

order = Resource('order', fields, get=get, post=post)

app = OctopusApp('autoDealer', [order], config)
app.run_server()