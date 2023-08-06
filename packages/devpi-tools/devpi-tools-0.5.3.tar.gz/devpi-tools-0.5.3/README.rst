devpi-tools
===========

|pypi|

Small Python library for interacting with devpi servers via web API

Installing
----------

.. code:: python

   pip install devpi-tools

Usage
-----

.. code:: python

   from devpi_tools import DevpiClient

   client = DevpiClient('http://127.0.0.1:3141')

   client.indexes() # list all indexes
   index = client.index('/root/pypi') # fetch a single index

   index.projects() # list all projects
   project = index.project('devpi-tools') # fetch a single project/package by name

   project.versions() # list of uploaded versions
   project.version('1.0.1') # fetch details on a specific version

Another example, finding the latest version of a specific package, in a
specific devpi index:

.. code:: python

   index = client.index('/root/pypi')
   v = index.project('requests').latest_version()
   print('version: %s' % v.version)
   print('uploaded: %s' % v.uploaded)

.. |pypi| image:: https://img.shields.io/pypi/v/devpi-tools?color=0b938a&logo=pypi&logoColor=%23ffffff&style=for-the-badge
   :target: https://pypi.org/project/devpi-tools/
