try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'ultracold-ions',
    'description': 'A library for the simulation of ultracold neutral plasmas.',
    'author': 'Tech-X Corporation',
    'url': 'https://github.com/Tech-XCorp/ultracold-ions',
    'download_url': 'https://github.com/Tech-XCorp/ultracold-ions',
    'author_email': 'dmeiser@txcorp.com',
    'version': '0.1',
    'install_requires': ['numpy','pyopencl','nose'],
    'packages': ['uci'],
    'scripts': []
}

setup(**config)
