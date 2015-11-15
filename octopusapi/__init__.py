import metadata
import json
import config
import logging
from wsgiref import simple_server
import falcon
from middleware import AuthMiddleware, RequireJSON, JSONTranslator, StorageError, max_body


__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright


class Field(object):
	def __init__(self, name, type, description, valid_values=None):
		self.name = name
		self.type = type
		self.description = description
		self.valid_values = valid_values


class Resource(object):
	def __init__(self, name, fields, get=None, post=None, put=None, delete=None, links=[]):
		self.name = name
		self.fields = fields
		self.links = links
		self.get = get
		self.post = post
		self.put = put
		self.delete = delete

	def validate_contract(self, req):
		fields = map(lambda field: field.name, self.fields)
		request_fields = req.context['doc'][self.name].keys()
		result = filter(lambda key: key in fields, request_fields)
		if len(result) != len(self.fields):
			raise falcon.HTTPBadRequest('Invalid input fields', 'The fields containing in the request body are not valid.')


	def on_get(self, req, resp, id=None):
		self.get(req, resp)

	@falcon.before(max_body(64 * 1024))
	def on_post(self, req, resp):
		self.validate_contract(req)
		self.post(req, resp)



class OctopusApp(object):
	def __init__(self, resources, config):
		self.resources = resources

	def validate_resource(self, resource):
		if not(resource.on_get or resource.on_post or resource.on_put or resource.on_delete):
			raise Exception('Resource {0} has no HTTP verb handling')
		pass

	def load_resource(self, app, resource):
		self.validate_resource(resource)
		app.add_route('/{0}/'.format(resource.name), resource)

	def run_server(self):
		app = falcon.API(middleware=[AuthMiddleware(), RequireJSON(), JSONTranslator()])
		map(lambda resource: self.load_resource(app, resource), self.resources)

		app.add_error_handler(StorageError, StorageError.handle)

		httpd = simple_server.make_server(config.host, config.port, app)
		httpd.serve_forever()