#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='django-query-parser',
    version='0.0.3',
    description='A django app to store and load partial queries from external  sources',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",

    author='Mohamed El-Kalioby',
    author_email = 'mkalioby@mkalioby.com',
    url = 'https://github.com/mkalioby/django-query-parser/',
    download_url='https://github.com/mkalioby/django-query-parser/',
    license='MIT',
    packages=find_packages('.','test_app'),
    install_requires=[],
    python_requires=">=3.5",
    include_package_data=True,
    zip_safe=True, # because we're including static files
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
]
)