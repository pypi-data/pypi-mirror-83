from setuptools import setup, find_packages

setup (
	name='datasetu',
	version='0.0.2',
	packages=find_packages(),
	install_requires=['requests', 'urllib3'],
	url='https://github.com/datasetu/datasetu-python',
	license='ISC',
	author='Datasetu Team',
	author_email='contact@artpark.in',
	description='Python SDK for DataSetu.'
)
