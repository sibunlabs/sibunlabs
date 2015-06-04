try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A collection of libraries for use in science.',
    'author': 'Basilius Sauter',
    'url': 'https://github.com/sibunlabs/sibunlabs',
    'version': '0.1',
    'install_requires': ['nose', 'numpy', 'cv2'],
    'packages': ['sibunlabs'],
    'scripts': [],
    'name': 'sibunlabs'
}

setup(**config)