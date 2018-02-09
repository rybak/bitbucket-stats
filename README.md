Bitbucket stats collector
=========================

[Bitbucket](https://www.atlassian.com/software/bitbucket) is a web-based
version control repository hosting service owned by Atlassian.

Note: only Bitbucket Server version 4.9.1 is supported.

Features
--------

At the moment, only display of open pull requests is supported.

Usage
-----

### Input

The script's input is provided through a `config.py` file.  Example is
provided in `config.py.sample`.  You need to provide:

* URL to the Bitbucket server
* your Bitbucket login to use with REST API
* Project key
* Repository name

Running
-------

After you filled in `config.py`:

    $ python collect.py

When the script starts downloading the list of pull requests, it will prompt
user for their Bitbucket password to authenticate with the Bitbucket server.

bb-stats uses Python 3 features and is not Python 2 compatible.


Dependencies
------------

* [requests](http://python-requests.org) library — to talk to a Bitbucket
  server via REST API

For details, see `Pipfile`.
