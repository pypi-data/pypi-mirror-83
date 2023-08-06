"""
A setup tools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/vesicash/vesicash-python
"""

from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vesicash-python',
    version='0.1.1-rc1',
    description='A python library to consume Vesicash API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vesicash/vesicash-python',

    # Author details
    author='Precious Opusunju',
    author_email='precious@vesicash.com',

    license='MIT',

    keywords='vesicash python library',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['requests'],

    extras_require={
        'test': ['coverage'],
    },
)