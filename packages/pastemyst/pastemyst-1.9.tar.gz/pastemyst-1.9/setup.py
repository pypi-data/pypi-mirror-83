from setuptools import setup

with open('README.md', 'r') as readme:
	desc = readme.read()

setup (
	name='pastemyst',
	version='1.9',
	packages=['pastemyst'],
	author='Munchii',
	author_email='daniellmunch@gmail.com',
	license='MIT',
	description='api wrapper for paste.myst.rs written in python',
	long_description=desc,
	long_description_content_type='text/markdown',
	url='https://github.com/Dmunch04/pastemyst-py',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: End Users/Desktop',
            	'Intended Audience :: Developers',
            	'License :: OSI Approved :: MIT License',
            	'Programming Language :: Python :: 3',
            	'Operating System :: OS Independent',
	],
	keywords='simple api wrapper python3 python pastemyst pastemyst.rs'
)
