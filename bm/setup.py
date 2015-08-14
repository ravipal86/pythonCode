# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

try:
    long_description = open('README.md', 'rt').read()
except IOError:
    long_description = ''

setup(
    name='bm',
    version='1.0',

    description='Search and Add Bookmarks of chrome from terminal',
    long_description=long_description,

    author='Ravi Pal',
    author_email='ravi_pal52@yahoo.co.in',

    url='https://github.com/ravipal86/pythonCode',
    download_url='https://github.com/ravipal86/pythonCode.git',

    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'beautifulsoup4',
        'lxml',
        'termcolor',
    ],
    entry_points='''
        [console_scripts]
        bm=bm.main:bm
    ''',
#    classifiers=[
#        'License :: OSI Approved :: Apache Software License',
#        'Programming Language :: Python',
#    ],
)