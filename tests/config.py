import os

def get_environment_variable(name):
	try:
		return os.environ[name]
	except:
		return None

host = get_environment_variable('HOST') or '127.0.0.1'
port = get_environment_variable('PORT') or 8000