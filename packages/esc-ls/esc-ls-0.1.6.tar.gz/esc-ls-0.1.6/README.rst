Escape sequence linting plugin for PYLS
=======================================

.. image:: https://badge.fury.io/py/esc-ls.svg
    :target: https://badge.fury.io/py/esc-ls

.. image:: https://github.com/Richardk2n/esc-ls/workflows/Python%20package/badge.svg?branch=master
    :target: https://github.com/Richardk2n/esc-ls/

This is a plugin for the Palantir's Python Language Server (https://github.com/palantir/python-language-server)

It, requires Python 3.6 or newer.


Installation
------------

Install into the same virtualenv as pyls itself.

``pip install esc-ls``

Configuration
-------------

Depending on your editor, the configuration (found in a file called esc-ls.cfg in your workspace or a parent directory) should be roughly like this:

::

    {
	"enabled": True
    }
