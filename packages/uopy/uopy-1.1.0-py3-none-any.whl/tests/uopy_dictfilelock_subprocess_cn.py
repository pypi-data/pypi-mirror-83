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

    def test_DictSubProc(self):
        # Lock a field in the dict file.
        # Prepare the test condition for "test_LockCheckForMulProcess" method's test under "TestDictFileClass" class
        dictFile = Dictionary("STATES_CP") 
        field = DynArray("")
        field.insert(1, "D")
        field.insert(2, "9")
        field.insert(3, "")
        field.insert(4, "dict测试")
        field.insert(5, "40L")
        field.insert(6, "S")
        dictFile.write("dict测试", field) 
        rec = dictFile.read("dict测试")
        self.assertEqual(str(rec[3]), "dict测试")       
            
        dictFile.lock("dict测试", uopy.LOCK_EXCLUSIVE)          

        # Check if the field is locked by subprocess
        result = dictFile.is_locked("dict测试")
        print('dictFile.is_locked("dict测试"):',str(result))
        self.assertEqual(result, True) 

        sleep(4) 
        dictFile.close()
                                                                                                  
if __name__ == '__main__':
    unittest.main()
