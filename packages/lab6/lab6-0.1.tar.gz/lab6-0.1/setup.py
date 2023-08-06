from setuptools import setup, find_packages
from os.path import join, dirname
setup(
    name='lab6',
    version='0.1',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'readme.md')).read(),
    entry_points={
        'console_scripts': [
            'start = package.__main__:start'
        ]
    }
)
