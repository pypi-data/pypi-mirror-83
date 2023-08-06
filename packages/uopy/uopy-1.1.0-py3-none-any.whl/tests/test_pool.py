# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

import unittest
from threading import Thread

import uopy
from tests.unitestbase import UniTestBase
from uopy import UOError, Command


@unittest.skipIf(not uopy.config.pooling["pooling_on"], "Pooling is not turned on.")
class TestPooling(UniTestBase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def create_test_case(self, buffer_size=None):
        with uopy.connect(**self.config) as session:
            command_text = 'LIST VOC'
            cmd = Command(command_text)
            if buffer_size:
                cmd.buffer_size = buffer_size
            cmd.run()
            self.assertTrue("LIST" in cmd.response[0:len(command_text)])

    def test_pooling_auto_recovery(self):
        thread_number = 20
        thread_list = []
        try:
            for i in range(thread_number):
                thread_list.append(Thread(target=self.create_test_case, kwargs={"buffer_size": 10}))

            for i in range(thread_number):
                thread_list[i].start()

            for i in range(thread_number):
                thread_list[i].join()

        except Exception as e:
            raise UOError(message=str(e))

    def test_pooling(self):
        thread_number = 100
        thread_list = []
        try:
            for i in range(thread_number):
                thread_list.append(Thread(target=self.create_test_case))

            for i in range(thread_number):
                thread_list[i].start()

            for i in range(thread_number):
                thread_list[i].join()

        except Exception as e:
            raise UOError(message=str(e))


if __name__ == '__main__':
    unittest.main()
