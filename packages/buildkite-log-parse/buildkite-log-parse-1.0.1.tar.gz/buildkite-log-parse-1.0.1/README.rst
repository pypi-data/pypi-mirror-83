buildkite-log-parse
==============

.. image:: https://badge.fury.io/py/buildkite-log-parse.png
    :target: https://badge.fury.io/py/buildkite-log-parse

.. image:: https://travis-ci.org/narfman0/buildkite-log-parse.png?branch=master
    :target: https://travis-ci.org/narfman0/buildkite-log-parse

Parse orgs pipelines for active build/job and parse string

Installation
------------

Install via pip::

    pip install buildkite-log-parse

Usage
-----

Example::

    buildkite-log-parse --organization org-1 \
        --pipeline bastion-server \
        --token qwertyuiopasdfghjklzxcvbnm1234567890asda \
        --regex "Access it for the next hour by running ssh (.*)" \
        --build_message "Common bastion.*" \
        --build_state "running" \
        --job "Run Server" \
        --group 1

Optionally add the `--debug` param to dump response logs

Development
-----------

Run test suite to ensure everything works::

    make test

Release
-------

To publish your plugin to pypi, sdist and wheels are registered, created and uploaded with::

    make release-test

For test. After ensuring the package works, run the prod target and win::

    make release-prod

License
-------

Copyright (c) 2020 Jon Robison

See LICENSE for details
