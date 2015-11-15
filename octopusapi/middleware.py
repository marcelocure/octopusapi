import json
import logging
import falcon


class StorageError(Exception):
    @staticmethod
    def handle(ex, req, resp, params):
        description = ('Sorry, could not store the message, it worked on my machine')
        raise falcon.HTTPError(falcon.HTTP_725, 'Database Error', description)


class AuthMiddleware(object):
    def process_request(self, req, resp):
		pass


class RequireJSON(object):
    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable('This API only supports responses encoded as JSON.')

        if req.method in ('POST'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType('This API only supports requests encoded as JSON.')


class JSONTranslator(object):

    def process_request(self, req, resp):
        if req.content_length in (None, 0):
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body', 'A valid JSON document is required.')

        try:
            req.context['doc'] = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753, 'Malformed JSON', 'Could not decode the request body. The JSON was incorrect or not encoded as UTF-8.')

    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return

        resp.body = json.dumps(req.context['result'])


def max_body(limit):
    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not exceed ' + str(limit) + ' bytes in length.')
            raise falcon.HTTPRequestEntityTooLarge('Request body is too large', msg)
    return hook
