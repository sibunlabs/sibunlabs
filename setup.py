try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A collection of libraries for use in science.',
    'author': 'Basilius Sauter',
    'url': 'https://github.com/sibunlabs/sibunlabs',
    'download_url': '',
    'author_email': '',
    'version': 'dev',
    'install_requires': ['nose', 'numpy', 'scipy'],
    'packages': ['sibunlabs'],
    'scripts': [],
    'name': 'sibunlabs'
}

setup(**config)