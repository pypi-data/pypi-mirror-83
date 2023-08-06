# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

import unittest

from tests.test_command import TestCommand
from tests.test_dictionary import TestDictionary
from tests.test_dynarray import TestDynArray
from tests.test_file import TestFile
from tests.test_list import TestList
from tests.test_pool import TestPooling
from tests.test_sequentialfile import TestSequentialFile
from tests.test_ssl import TestSsl
from tests.test_subroutine import TestSubroutine
from tests.test_transaction import TestTransaction

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCommand))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDictionary))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDynArray))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestFile))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestList))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPooling))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSequentialFile))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSsl))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSubroutine))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTransaction))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
