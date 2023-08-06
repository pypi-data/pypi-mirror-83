# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

from uopy import UOError
from tests.unitestbase import *


class TestTransaction(UniTestBase):

    def setUp(self):
        super().setUp()
        self.create_test_file('FOOBAR')

    def tearDown(self):
        self.delete_test_file('FOOBAR')
        return super().tearDown()

    def test_transaction(self):
        self.assertFalse(self.session.tx_is_active())

        self.session.tx_start()
        self.assertTrue(self.session.tx_is_active())

        with File('FOOBAR') as test_file:
            test_file.write('REC1', 'D1')
            test_file.write('REC2', 'D2')

            if self.session.db_type == "UV":
                self.session.tx_start()
                tx_level = self.session.tx_level()
                self.assertEqual(tx_level, 2)
                self.session.tx_rollback()

        self.session.tx_rollback()
        if self.session.db_type == "UV":
            tx_level = self.session.tx_level()
            self.assertEqual(tx_level, 0)

        with File('FOOBAR') as test_file:
            with self.assertRaises(UOError):
                test_file.read("REC1")
                test_file.read("REC2")

            self.session.tx_start()
            test_file.write("REC3", "D3")
            test_file.write("REC4", "D4")
            self.session.tx_commit()

        with File('FOOBAR') as test_file:
            r3 = test_file.read("REC3")
            r4 = test_file.read('REC4')
            self.assertEqual(str(r3), 'D3')
            self.assertEqual(str(r4), 'D4')


if __name__ == '__main__':
    unittest.main()
