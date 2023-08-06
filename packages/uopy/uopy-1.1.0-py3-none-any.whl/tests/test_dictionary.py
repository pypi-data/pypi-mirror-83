# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

import unittest

from uopy import Dictionary
from tests.unitestbase import UniTestBase


class TestDictionary(UniTestBase):

    def setUp(self):
        super().setUp()
        self.create_test_file('FOOBAR')
        self.record_id = "F1"
        self.file_name = "FOOBAR"

        self.dict_file = Dictionary(self.file_name)

        self.dict_file.set_assoc(self.record_id, '')
        self.dict_file.set_loc(self.record_id, 1)
        self.dict_file.set_conv(self.record_id, '')
        self.dict_file.set_sql_type(self.record_id, '')
        self.dict_file.set_format(self.record_id, '15T')
        self.dict_file.set_type(self.record_id, 'D')
        self.dict_file.set_name(self.record_id, '')

    def tearDown(self):
        self.dict_file.close()
        self.delete_test_file("FOOBAR")
        super().tearDown()

    def test_dictionary(self):
        # read old values
        actual_assoc = str(self.dict_file.get_assoc(self.record_id))
        actual_loc = str(self.dict_file.get_loc(self.record_id))
        actual_conv = str(self.dict_file.get_conv(self.record_id))
        actual_sql_type = str(self.dict_file.get_sql_type(self.record_id))
        actual_format = str(self.dict_file.get_format(self.record_id))
        actual_type = str(self.dict_file.get_type(self.record_id))
        actual_name = str(self.dict_file.get_name(self.record_id))
        actual_sm = str(self.dict_file.get_sm(self.record_id))

        # test the write operations
        self.dict_file.set_assoc(self.record_id, "TEST_ASSOC")
        self.dict_file.set_loc(self.record_id, 20)
        self.dict_file.set_conv(self.record_id, 'P(6N)')
        self.dict_file.set_sql_type(self.record_id, '1')
        self.dict_file.set_format(self.record_id, '25L')
        self.dict_file.set_type(self.record_id, 'I')
        self.dict_file.set_name(self.record_id, 'testname')
        self.dict_file.set_sm(self.record_id, 'M')

        # get the new values
        new_assoc = self.dict_file.get_assoc(self.record_id, )
        new_loc = self.dict_file.get_loc(self.record_id, )
        new_conv = self.dict_file.get_conv(self.record_id, )
        new_sqlt = self.dict_file.get_sql_type(self.record_id, )
        new_fmt = self.dict_file.get_format(self.record_id, )
        new_type = self.dict_file.get_type(self.record_id, )
        new_name = self.dict_file.get_name(self.record_id, )
        new_sm = self.dict_file.get_sm(self.record_id, )

        # restore the modified values
        self.dict_file.set_assoc(self.record_id, actual_assoc)
        self.dict_file.set_loc(self.record_id, actual_loc)
        self.dict_file.set_conv(self.record_id, actual_conv)
        self.dict_file.set_sql_type(self.record_id, actual_sql_type)
        self.dict_file.set_format(self.record_id, actual_format)
        self.dict_file.set_type(self.record_id, actual_type)
        self.dict_file.set_name(self.record_id, actual_name)
        self.dict_file.set_sm(self.record_id, actual_sm)

        # check the results
        self.assertEqual(new_assoc, 'TEST_ASSOC')
        self.assertEqual(new_loc, '20')
        self.assertEqual(new_conv, 'P(6N)')
        self.assertEqual(new_sqlt, '1')
        self.assertEqual(new_fmt, '25L')
        self.assertEqual(new_type, 'I')
        self.assertEqual(new_name, 'testname')
        self.assertEqual(new_sm, 'M')


if __name__ == '__main__':
    unittest.main()
