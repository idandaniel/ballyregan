Usage
=====

.. _installation:

Installation
------------

To use Ballyregan, first install it using pip:

.. code-block:: console

   (.venv) $ pip install ballyregan

Getting a proxy
----------------

First of all, you need to create a fetcher instance:

>>> from ballyregan import ProxyFetcher
>>> fetcher = ProxyFetcher()

you can use the ``fetcher.get_one()`` function:

.. autofunction:: fetcher.get_one

The ``limit`` is the max amount of proxies you want to get,
you can also filter by ``protocols`` and ``anonymities``.

to get more than one proxy, you can use the ``fetcher.get()`` function:

.. autofunction:: fetcher.get_one


For example:

>>> import lumache
>>> lumache.get_random_ingredients()
['shells', 'gorgonzola', 'parsley']

