# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

from uopy import UOError, EXEC_MORE_OUTPUT, SequentialFile, Command, Dictionary, File, DynArray, Subroutine
from tests.unitestbase_cn import *
import os
import struct
from time import sleep

class TestFileCn(UniTestBaseCn):
    session = None

    def setUp(self):
        super().setUp()
        
    def tearDown(self):
        super().tearDown()

    def test_DataSubProc(self):
            # Lock a record in the data file.
            # Prepare the test condition for "test_LockCheckForMulProcess" method's test under "TestDataFileClass" class
            stt = File("STATES_CP")           
            stt.lock("BJ", uopy.LOCK_EXCLUSIVE)
            result = stt.is_locked("BJ")
            self.assertEqual(result, True)

            sleep(4) 
            stt.close()
                                                                                                  
if __name__ == '__main__':
    unittest.main()
