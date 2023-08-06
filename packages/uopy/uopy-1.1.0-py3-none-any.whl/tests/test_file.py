# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

import threading
import unittest
from time import sleep
from timeit import Timer

from uopy import DynArray
from uopy import EXEC_COMPLETE
from uopy import File, Command, UOError
from uopy import LOCK_EXCLUSIVE, LOCK_RETAIN, LOCK_SHARED, LOCK_WAIT, List
from tests.unitestbase import UniTestBase


class TestFile(UniTestBase):

    def setUp(self):
        super().setUp()
        self.create_test_file('FOOBAR')

        # create i_type
        if not self.session.db_type == 'D3':
            cmd = Command()
            cmd.command_text = "CREATE.INDEX FOOBAR @ID"
            cmd.run()

            while cmd._status != EXEC_COMPLETE:
                cmd.reply("")

        test_file = File("FOOBAR")
        for idx in range(1, 30):
            str_idx = str(idx)
            test_file.write("REC" + str_idx, "DATA" + str_idx)

        test_file.close()

    def tearDown(self):
        self.delete_test_file("FOOBAR")
        super().tearDown()

    def test_clear_file(self):
        with File("FOOBAR") as test_file:
            test_file.write("TESTCLEAR", "PYTHON")
            test_file.clear()
            self.assertRaises(UOError, test_file.read, "TESTCLEAR")

    def test_read(self):
        with File("FOOBAR") as test_file:
            rec = test_file.read("REC1")
            self.assertTrue(rec == "DATA1")
            rec = test_file.read("REC2", LOCK_EXCLUSIVE)
            self.assertFalse(test_file.is_locked("REC1"))
            self.assertTrue(test_file.is_locked("REC2"))
            rec = test_file.read("REC3", LOCK_SHARED)
            self.assertTrue(test_file.is_locked("REC3"))

    def test_locking(self):
        with File("FOOBAR") as test_file:
            rec = test_file.read("REC2", LOCK_EXCLUSIVE)
            self.assertTrue(test_file.is_locked("REC2"))
            test_file.write("REC2", rec)
            self.assertTrue(not test_file.is_locked("REC2"))
            test_file.lock("REC2")
            test_file.write("REC2", rec, LOCK_RETAIN)
            self.assertTrue(test_file.is_locked("REC2"))

    def lock_and_sleep(self, hold_time=0):
        with self.get_session() as session:
            with File("FOOBAR", session=session) as test_file:
                rec = test_file.read("REC2", LOCK_EXCLUSIVE)
                self.assertTrue(test_file.is_locked("REC2"))
                sleep(hold_time)
                test_file.unlock("REC2")

    def wait_and_write(self):
        with File("FOOBAR", session=self.session) as test_file:
            test_file.write("REC2", "data", LOCK_WAIT)

    def test_multi_user_locking(self):
        locking_thread = threading.Thread(target=self.lock_and_sleep, kwargs={"hold_time": 5})

        locking_thread.start()
        sleep(2)
        time_used = Timer(self.wait_and_write).timeit(number=1)

        self.assertGreaterEqual(time_used + 2, 5)
        locking_thread.join()

    def lock_file_and_sleep(self, hold_time=0):
        with self.get_session() as session:
            with File("FOOBAR", session=session) as test_file:
                test_file.lock_file()
                sleep(hold_time)
                test_file.unlock_file()

    def test_lock_file(self):
        locking_thread = threading.Thread(target=self.lock_file_and_sleep, kwargs={"hold_time": 5})

        locking_thread.start()
        sleep(2)

        with File("FOOBAR") as test_file:
            self.assertRaises(UOError, test_file.write, "TEST2", "LOCK")

        locking_thread.join()

    def test_delete(self):
        with File("FOOBAR") as test_file:
            test_file.write("TEST1", "JAVA1")
            test_file.delete("TEST1")
            self.assertRaises(UOError, test_file.delete, "TEST1")

    def test_file_opened(self):
        test_file = File("FOOBAR")
        self.assertTrue(test_file.is_opened)

        test_file.close()
        self.assertFalse(test_file.is_opened)

    def test_get_ak_info(self):
        with File("FOOBAR") as test_file:
            ak_info = test_file.get_ak_info()
            self.assertEqual(ak_info, "@ID")
            self.assertIsInstance(ak_info, DynArray)

    def test_is_locked(self):
        with File("FOOBAR") as test_file:
            test_file.write("LOCKIT", "LOCKIT")
            test_file.write("NOTLOCKED", "NOTLOCKED")
            test_file.lock("LOCKIT", LOCK_EXCLUSIVE)
            self.assertTrue(test_file.is_locked("LOCKIT"))
            self.assertFalse(test_file.is_locked("NOTLOCKED"))

    def test_itype(self):
        if self.session.db_type == "UV":
            file_name = "VOC"
            rec_id = "LIST.INDEX"
            itype_id = "SIZE"
        else:
            cmd = Command("COMPILE.DICT AE_DOC")
            cmd.run()
            file_name = "AE_DOC"
            rec_id = "FORMAT"
            itype_id = "LAST.LINE"

        with File(file_name) as test_file:
            itype_value = test_file.itype(rec_id, itype_id)
            self.assertIsInstance(itype_value, DynArray)
            test_file.close()

    def test_open(self):
        test_file = File("FOOBAR")
        test_file.close()
        self.assertRaises(UOError, File, "NOSUCHFILE")

    def test_read_field(self):
        with File("FOOBAR") as test_file:
            test_file.write("TESTREADFIELD", ["abc", "def", ['1', '2', '3']])
            rec = test_file.read("TESTREADFIELD")
            self.assertEqual(rec, ["abc", "def", ['1', '2', '3']])
            fld = test_file.read_field("TESTREADFIELD", 1)
            self.assertTrue(fld == ["abc"])
            self.assertTrue(["abc"], fld)
            fld = test_file.read_field("TESTREADFIELD", 2)[0]
            self.assertTrue(fld == "def")
            fld = test_file.read_field("TESTREADFIELD", 3)
            self.assertTrue(fld == [['1', '2', '3']])

    def test_write_field(self):
        with File("FOOBAR") as test_file:
            test_file.write_field("TESTREADFIELD", 3, [['1', '2', '3']])
            rec = test_file.read("TESTREADFIELD")
            self.assertTrue(rec == ["", "", ['1', '2', '3']])
            # fld = test_file.read_field("TESTREADFIELD", 3)
            # self.assertTrue(fld == [['1', '2', '3']])

    def test_read_named_fields(self):
        with File("RENTAL_DETAILS") as test_file:
            field_list = ["BAD_FIELD_NAME", "FULL_NAME", "ACTUAL_COST", "ACTUAL_RETURN_DATE", "BALANCE_DUE"]
            id_list = List().select(test_file).read_list()
            id_list = ['1084', '1307', '1976']
            id_list.insert(0, "BAD_RECID_1")
            id_list.insert(0, "BAD_RECID_2")
            id_list.insert(0, "BAD_RECID_3")
            read_rs = test_file.read_named_fields(id_list, field_list)

            success_count = sum(x == '0' for x in read_rs[0])
            self.assertEqual(success_count, len(id_list) - 3)
            failure_count = sum(x != '0' for x in read_rs[0])
            self.assertEqual(failure_count, 3)

            good_recs = [(x[1], x[2]) for x in zip(read_rs[0], read_rs[2], read_rs[3]) if x[0] == '0']
            for rec_id, rec in good_recs:
                self.assertEqual(rec_id, rec[0])

    def test_write_named_fields(self):
        with File("PRODUCTS") as test_file:
            field_list = ["TITLE", "ACTOR", "DIRECTOR", "THEATERDATE", "LOCATION"]
            id_list = List().select(test_file).read_list()
            read_rs = test_file.read_named_fields(id_list, field_list)
            rec_list = read_rs[3]
            self.assertEqual(len(rec_list), len(id_list))

            write_rs = test_file.write_named_fields(id_list, field_list, rec_list)
            good_recs = [(x[1], x[2]) for x in zip(write_rs[0], write_rs[2], write_rs[3]) if x[0] == '0']
            self.assertEqual(len(good_recs), len(id_list))

            rs_aft_write = test_file.read_named_fields(id_list, field_list)
            self.assertEqual(read_rs, rs_aft_write)

    def test_read_records(self):
        with File("RENTAL_DETAILS") as test_file:
            id_list = List().select(test_file).read_list()
            id_list.insert(0, "BAD_RECID_1")
            id_list.insert(0, "BAD_RECID_2")
            id_list.insert(0, "BAD_RECID_3")
            read_rs = test_file.read_records(id_list)
            success_count = sum(x == '0' for x in read_rs[0])
            self.assertEqual(success_count, len(id_list) - 3)
            failure_count = sum(x != '0' for x in read_rs[0])
            self.assertEqual(failure_count, 3)

    def test_write_records(self):
        with File("PRODUCTS") as test_file:
            id_list = List().select(test_file).read_list()
            read_rs = test_file.read_records(id_list)
            rec_list = read_rs[3]
            self.assertEqual(len(rec_list), len(id_list))

            write_result_set = test_file.write_records(id_list, rec_list)

            good_recs = [(x[1], x[2]) for x in zip(write_result_set[0], write_result_set[2], write_result_set[3]) if x[0] == '0']
            self.assertEqual(len(good_recs), len(id_list))

            rs_aft_write = test_file.read_records(id_list)
            for i in range(0, 4):
                self.assertEqual(read_rs[i], rs_aft_write[i])


if __name__ == '__main__':
    unittest.main()
