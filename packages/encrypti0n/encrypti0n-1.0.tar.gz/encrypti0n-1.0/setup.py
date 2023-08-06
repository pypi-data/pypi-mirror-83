# source: https://python-packaging.readthedocs.io/en/latest/minimal.html
from setuptools import setup
setup(
	name='encrypti0n',
	version='1.0',
	description='Easily encrypt & decrypt files with python / through the CLI.',
	url='http://github.com/vandenberghinc/encrypti0n',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=['encrypti0n'],
	zip_safe=True)