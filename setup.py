# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name = 'pyboleto',
    version = __import__('pyboleto').__version__,
    author = 'Eduardo Cereto Carvalho',
    author_email = 'eduardocereto@gmail.com',
    url = 'https://bitbucket.org/eduardo.cereto/pyboleto/',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'reportlab>=2.5',
    ],
    provides = [
        'pyboleto'
    ],
    license = 'BSD',
    description = 'Python Library to create boletos',
    long_description = open('README.rst', 'r').read(),
    download_url = 'http://pypi.python.org/pypi/pyboleto',
    entry_points = {
        'console_scripts':[
            'print_boleto_data = pyboleto.scripts.print_sample_data:print_test',
        ],
    },
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Portuguese (Brazilian)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

