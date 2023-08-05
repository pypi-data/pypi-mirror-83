import doctest
import unittest

import hyperdiary.simplepath
import hyperdiary.diary
import hyperdiary.localization

suite = unittest.TestSuite()
suite.addTest(doctest.DocTestSuite(hyperdiary.htmltags))
suite.addTest(doctest.DocTestSuite(hyperdiary.simplepath))
suite.addTest(doctest.DocTestSuite(hyperdiary.diary))
suite.addTest(doctest.DocTestSuite(hyperdiary.tiddlywiki))
suite.addTest(doctest.DocTestSuite(hyperdiary.localization))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
