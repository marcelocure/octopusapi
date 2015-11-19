# Octopus API
Python engine to build rest API's based on Falcon.

Installation:

1) install falcom as per its docs http://falcon.readthedocs.org/en/latest/user/install.html
2) pip install -r requirements-dev.txt


Some octopusapi goals:

1) Create multiple endpoints;
2) Create contract with field validation;
3) Easily setup;
4) Performance;


Usage:

from octopusapi import Resource, Field, OctopusApp
import config
import falcon


fields = []
fields.append(Field(name='serialNumber', type='string', description='Device serial number'))
fields.append(Field(name='status', type='string', description='Order status', valid_values=['processing', 'error', 'completed']))
fields.append(Field(name='activationLocation', type='string', description='Activation Location'))

def get(request, response):
	response.body = 'fuck yeahhh!!'
	response.status = falcon.HTTP_200

def post(request, response):
	response.status = falcon.HTTP_200

order = Resource('order', fields, get=get, post=post)

app = OctopusApp([order], config)
app.run_server()