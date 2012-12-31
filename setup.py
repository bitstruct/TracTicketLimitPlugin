#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'TracTicketLimit',
    version = '0.2',
    author = 'Rob Emanuele',
    author_email = 'rje@bitstruct.com',
    maintainer = 'Rob Emanuele',
    maintainer_email = 'rje@bitstruct.com',
    description = 'Limit Ticket Creation on a Time Schedule Per Component',
    license = 'Apache',
    zip_safe=True,

    packages=['tracticketlimit'],
    package_data = { 'tracticketlimit': [ '*.txt' ] },

    classifiers = [
        'Framework :: Trac',
    ],

    keywords="ticket",
    install_requires = [],
    entry_points = {'trac.plugins': ['tracticketlimit = tracticketlimit.main']},
)
