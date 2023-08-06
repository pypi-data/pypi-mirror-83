import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name = 'htmhelloworld', #name on Pypi
	version = '0.0.7', # 0.0.x says it is unstable
	description = 'Say Hello',
	author = 'htm',
	author_email ='htm@htm.com',
	url = '',
	long_description = long_description,
	long_description_content_type = "text/markdown",
	#packages=['htmhelloworld'],
	py_modules = ["helloworld_1", "helloworld_2"]
	#package_dir = {'':'src'}
	)