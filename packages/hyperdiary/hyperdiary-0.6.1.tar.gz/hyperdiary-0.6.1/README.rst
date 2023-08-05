============
hyperdiary
============

.. image:: https://img.shields.io/pypi/v/hyperdiary.svg
        :target: https://pypi.python.org/pypi/hyperdiary

.. image:: https://travis-ci.com/luphord/hyperdiary.svg
        :target: https://travis-ci.com/luphord/hyperdiary

.. image:: https://readthedocs.org/projects/hyperdiary/badge/?version=latest
        :target: https://hyperdiary.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

A command line tool for writing diaries with hyperlinks. Free software, licensed under MIT license.

Installation
------------

hyperdiary requires Python version 3.5 or later. Once you have Python and pip installed on your machine (and available in your path) you can install hyperdiary by executing

.. code-block:: console

        pip install hyperdiary

Setup
-----

A project file *hyperdiary.json* is required to setup your diary. It should be of this form:

.. code-block:: json

        {
                "sources": [
                        "2019/05.yaml",
                        "2019/06.yaml"
                ],
                "expected": [
                        {"start": "2019-05-01", "end": "2019-05-01"},
                        {"start": "2019-06-09", "end": "2019-06-10"}
                ],
                "localization": {
                        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                        "date_fmt": "%-d.%-m.%Y"
                }
        }

You diary content itself is entered in yaml files like this (*2019/06.yaml*):

.. code-block:: yaml

        2019-06-09:
          - Some entry goes here with a $special_identity|link
          - This entry is +surprise tagged +mytag +nexttag
          - This entry contains nothing new
        2019-06-10:
          - Same $special_identity|link again and $New_Identity|NewIdentity
          - $test +mytag

Use *$target|linktext* to create a hyperlink to *target* showing text *linktext*. Use *+mytag* to add tag *mytag*.

Usage
-----

.. code-block:: console

        usage: hyperdiary [-h]
                  {check,stats,html,htmlfolder,hugo,tiddlers,tiddlywiki,view}
                  ...

        The hyperdiary main command line interface.

        optional arguments:
                -h, --help            show this help message and exit

        subcommands:
                {check,stats,html,htmlfolder,hugo,tiddlers,tiddlywiki,view}
                                        Available subcommands
                check               Check entire diary for integrity up-to-dateness
                stats               Calculate impressive diary statistics
                html                Export diary to html
                htmlfolder          Export diary to html in folders
                hugo                Export diary to hugo static site format
                tiddlers            Export diary to tiddlywiki tiddlers format
                tiddlywiki          Export diary to tiddlywiki
                view                View entries on command line