=======
History
=======

0.6.1 (2020-10-21)
------------------

* add support for Python 3.8
* upgrade to flake8 3.8.4 and fix linter issues
* replace deprecated test command
* move to travis-ci.com

0.6.0 (2019-11-29)
------------------

* promote status to alpha
* introduced localization using hyperdiary.json; date format and month names so far
* added tiddlers for month (calendar) and year overview with hyperlinks
* Diary supports iteration by year/month
* make docs work

0.5.0 (2019-11-06)
------------------

* removed EntryType, refactored iteration, primarily passing Diary instances around
* fix bug when an ID is followed by a bracket )
* only line entries are allowed, no more dicts

0.4.0 (2019-10-30)
------------------

* full type annotations added for package
* linting and type checking in CI
* EntryTypes Dict and DictLine are deprecated and will be removed in 0.5 (check issues a warning)

0.3.2 (2019-10-17)
------------------

* fix linter configuration (and activate it)
* make all hyperdiary source files PEP8 conform
* set up bumpversion config

0.3.1 (2019-07-03)
------------------

* open date ranges iterate until yesterday, not today
* fix loading hyperdiary.json without expected field

0.3.0 (2019-06-19)
------------------

* Expected date ranges for check subcommand can be specified
* subcommand for export to tiddlywiki
* Tests for various output formats

0.2.0 (2019-06-12)
------------------

* stats subcommand can be invoked for all entries
* Rename `tiddlywiki` subcommand to `tiddlers` for different future usage
* Integrate Travis CI for automated testing
* Add basic tests
* Refactor diary/entry passing to subcommands

0.1.2 (2019-06-11)
------------------

* Fix htmlfolder subcommand by packaging picnic.min.css
* Fix view subcommand by using correct relative import
* Avoid deprecation warning in stats subcommand by using yaml.SafeLoader

0.1.1 (2019-04-29)
------------------

* Fix setup

0.1.0 (2019-04-28)
------------------

* First release on PyPI
* Import from fossil
