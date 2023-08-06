from setuptools import setup, find_packages

setup(
	name							= 'miva-mmt',
	version							= '1.0.1',
	author							= 'Miva, Inc.',
	author_email					= 'support@miva.com',
	packages						= find_packages( exclude = [ 'test' ] ),
	entry_points					= { 'console_scripts': [ 'mmt = mmt:main' ] },
	url								= 'https://docs.miva.com/template-branches/template-branches-overview#mmt_overview',
	install_requires				= [ 'merchantapi>=2.0.1' ],
	python_requires					= '>=3.6',
	license							= 'MMT License Agreement',
	long_description				= open( 'README.md', encoding = 'utf-8' ).read().strip(),
	long_description_content_type	= 'text/markdown',
	description						= 'Miva Managed Templates (MMT)'
)
