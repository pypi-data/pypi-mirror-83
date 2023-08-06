# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

from uopy import List, DynArray
from tests.unitestbase import *


class TestList(UniTestBase):

    def test_existing_list(self):
        cmd = Command("SELECT VOC WITH F1 = 'V'")
        cmd.run()
        select_list = List()
        ids = select_list.read_list()
        self.assertGreater(len(ids), 0)

    def test_read_list(self):
        with File("PRODUCTS") as file:
            select_list = List().select(file)
            ids = select_list.read_list()
            self.assertIsInstance(ids, DynArray)
            self.assertGreater(len(ids), 0)

    def test_iteration(self):
        with File("PRODUCTS") as file:
            select_list = List(9).select(file)
            for rec_id in select_list:
                fld = file.read_field(rec_id, 0)
                self.assertEqual(fld, rec_id)

    def test_error_listno(self):
        self.assertRaises(UOError, List, 11)

    def test_clear(self):
        with File("PRODUCTS") as file:
            select_list = List().select(file)
            select_list.clear()
            self.assertIsNone(select_list.next())

    def test_form_list(self):
        with File("PRODUCTS") as file:
            ids = List().select(file).read_list()
            first_50_ids = ids[:50]
            select_list = List()
            select_list.form_list(first_50_ids)
            for rec_id in select_list:
                fld = file.read_field(rec_id, 0)
                self.assertEqual(fld, rec_id)

    def test_ak_select(self):
        self.create_test_index_file("RENTAL_DETAILS", "CUSTOMER_CODE")

        with File("RENTAL_DETAILS") as file:
            select_list = List().select_alternate_key(file, "CUSTOMER_CODE")
            ids = select_list.read_list()
            self.assertGreater(len(ids), 0)

        self.delete_test_index_file("RENTAL_DETAILS", "CUSTOMER_CODE")

    def test_ak_matching_select(self):
        self.create_test_index_file("RENTAL_DETAILS", "CUSTOMER_CODE")

        # TODO a possible bug on the server side, never been tested before
        with self.assertRaises(UOError):
            with File("RENTAL_DETAILS") as file:
                select_list = List().select_matching_ak(file, "CUSTOMER_CODE", "0004")
                ids = select_list.read_list()
                self.assertEqual(len(ids), 1)
                self.assertGreater(len(ids), 0)

            self.delete_test_index_file("RENTAL_DETAILS", "CUSTOMER_CODE")


if __name__ == '__main__':
    unittest.main()
