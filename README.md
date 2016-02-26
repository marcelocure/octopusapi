<img src="https://travis-ci.org/marcelocure/octopusapi.svg"/>

# Octopus API
Python engine to build rest API's based on Falcon.

# Installation:

please refer to https://github.com/marcelocure/octopusapi/blob/master/.travis.yml for installation steps

Some octopusapi goals:

1) Create multiple endpoints;

2) Create contract;

3) Contract input validation already embeded on the API;

4) Easily setup;

5) Performance.

# Usage: 

```python

from octopusapi import Resource, Field, OctopusApp
import config
import falcon


fields = []
fields.append(Field(name='name', type='string', description='dealer name'))
fields.append(Field(name='status', type='string', description='status', valid_values=['active', 'inactive']))

def get(request, response):
	print request
	response.body = 'yeahhh!!'
	response.status = falcon.HTTP_200

def post(request, response):
	print request
	response.status = falcon.HTTP_200

dealer = Resource('dealer', fields, get=get, post=post)

app = OctopusApp('dealership-api', [dealer], config)
app.run_server()
```

https://github.com/marcelocure/octopusapi/blob/master/examples/main.py
