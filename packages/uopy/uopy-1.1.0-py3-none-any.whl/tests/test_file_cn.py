# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

#coding=utf-8
from uopy import UOError, EXEC_MORE_OUTPUT, SequentialFile, Command, Dictionary, File, DynArray, Subroutine
from tests.unitestbase_cn import *
import os
import struct
import platform
import subprocess
import sys
from time import sleep

class TestFileCn(UniTestBaseCn):
    session = None

    def setUp(self):
        super().setUp()
        self.create_test_file3('STATES_CP')
        self.file_name = "STATES_CP"
        self.field_id0 = "@ID"
        self.field_id1 = "STATES_CP_CODE"
        self.field_id2 = "STATES_CP_PK"
        self.field_id3 = "ID"
        self.field_id4 = "NAME"
        self.field_id5 = "STATE_NAME"
        self.field_id6 = "REGION"
        self.field_id7 = "DIVISION"
        self.field_id8 = "AMENDED_BY"
        self.field_id9 = "AMENDED_DATE"
        self.field_id10 = "@"
        self.field_id11 = "AMEND_INFO"
        
        self.dict_file = Dictionary(self.file_name)

        self.dict_file.set_type(self.field_id0, 'D')
        self.dict_file.set_loc(self.field_id0, 0)
        self.dict_file.set_conv(self.field_id0, '')
        self.dict_file.set_name(self.field_id0, '州编号')
        self.dict_file.set_format(self.field_id0, '20L')
        self.dict_file.set_sm(self.field_id0, 'S')
        self.dict_file.set_assoc(self.field_id0, '')
        self.dict_file.set_sql_type(self.field_id0, '')

        self.dict_file.set_type(self.field_id1, 'D')
        self.dict_file.set_loc(self.field_id1, 0)
        self.dict_file.set_conv(self.field_id1, '')
        self.dict_file.set_name(self.field_id1, '州编号')
        self.dict_file.set_format(self.field_id1, '20L')
        self.dict_file.set_sm(self.field_id1, 'S')
        self.dict_file.set_assoc(self.field_id1, '')
        self.dict_file.set_sql_type(self.field_id1, '')

        self.dict_file.set_type(self.field_id2, 'D')
        self.dict_file.set_loc(self.field_id2, 0)
        self.dict_file.set_conv(self.field_id2, '')
        self.dict_file.set_name(self.field_id2, '州编号')
        self.dict_file.set_format(self.field_id2, '20L')
        self.dict_file.set_sm(self.field_id2, 'S')
        self.dict_file.set_assoc(self.field_id2, '')
        self.dict_file.set_sql_type(self.field_id2, '')

        self.dict_file.set_type(self.field_id3, 'D')
        self.dict_file.set_loc(self.field_id3, 0)
        self.dict_file.set_conv(self.field_id3, '')
        self.dict_file.set_name(self.field_id3, '州编号')
        self.dict_file.set_format(self.field_id3, '20L')
        self.dict_file.set_sm(self.field_id3, 'S')
        self.dict_file.set_assoc(self.field_id3, '')
        self.dict_file.set_sql_type(self.field_id3, '')

        self.dict_file.set_type(self.field_id4, 'D')
        self.dict_file.set_loc(self.field_id4, 1)
        self.dict_file.set_conv(self.field_id4, '')
        self.dict_file.set_name(self.field_id4, '州名')
        self.dict_file.set_format(self.field_id4, '20L')
        self.dict_file.set_sm(self.field_id4, 'S')
        self.dict_file.set_assoc(self.field_id4, '')
        self.dict_file.set_sql_type(self.field_id4, '')

        self.dict_file.set_type(self.field_id5, 'D')
        self.dict_file.set_loc(self.field_id5, 1)
        self.dict_file.set_conv(self.field_id5, '')
        self.dict_file.set_name(self.field_id5, '州名')
        self.dict_file.set_format(self.field_id5, '20L')
        self.dict_file.set_sm(self.field_id5, 'S')
        self.dict_file.set_assoc(self.field_id5, '')
        self.dict_file.set_sql_type(self.field_id5, '')

        self.dict_file.set_type(self.field_id6, 'D')
        self.dict_file.set_loc(self.field_id6, 2)
        self.dict_file.set_conv(self.field_id6, '')
        self.dict_file.set_name(self.field_id6, '地区')
        self.dict_file.set_format(self.field_id6, '30L')
        self.dict_file.set_sm(self.field_id6, 'S')
        self.dict_file.set_assoc(self.field_id6, '')
        self.dict_file.set_sql_type(self.field_id6, '')

        self.dict_file.set_type(self.field_id7, 'D')
        self.dict_file.set_loc(self.field_id7, 3)
        self.dict_file.set_conv(self.field_id7, '')
        self.dict_file.set_name(self.field_id7, '行政区域')
        self.dict_file.set_format(self.field_id7, '30L')
        self.dict_file.set_sm(self.field_id7, 'S')
        self.dict_file.set_assoc(self.field_id7, '')
        self.dict_file.set_sql_type(self.field_id7, '')

        self.dict_file.set_type(self.field_id8, 'D')
        self.dict_file.set_loc(self.field_id8, 4)
        self.dict_file.set_conv(self.field_id8, '')
        self.dict_file.set_name(self.field_id8, '修改')
        self.dict_file.set_format(self.field_id8, '30L')
        self.dict_file.set_sm(self.field_id8, 'M')
        self.dict_file.set_assoc(self.field_id8, '')
        self.dict_file.set_sql_type(self.field_id8, '')

        self.dict_file.set_type(self.field_id9, 'D')
        self.dict_file.set_loc(self.field_id9, 5)
        self.dict_file.set_conv(self.field_id9, 'D4')
        self.dict_file.set_name(self.field_id9, '修改日期')
        self.dict_file.set_format(self.field_id9, '30R')
        self.dict_file.set_sm(self.field_id9, 'M')
        self.dict_file.set_assoc(self.field_id9, '')
        self.dict_file.set_sql_type(self.field_id9, '')

        self.dict_file.set_type(self.field_id10, 'PH')
        self.dict_file.set_loc(self.field_id10, "NAME REGION DIVISION AMENDED_BY AMENDED_DATE")
        self.dict_file.set_conv(self.field_id10, '')
        self.dict_file.set_name(self.field_id10, '')
        self.dict_file.set_format(self.field_id10, '')
        self.dict_file.set_sm(self.field_id10, '')
        self.dict_file.set_assoc(self.field_id10, '')
        self.dict_file.set_sql_type(self.field_id10, '')

        self.dict_file.set_type(self.field_id11, 'PH')
        self.dict_file.set_loc(self.field_id11, "AMENDED_BY AMENDED_DATE")
        self.dict_file.set_conv(self.field_id11, '')
        self.dict_file.set_name(self.field_id11, '')
        self.dict_file.set_format(self.field_id11, '')
        self.dict_file.set_sm(self.field_id11, '')
        self.dict_file.set_assoc(self.field_id11, '')
        self.dict_file.set_sql_type(self.field_id11, '')
        
        self.dict_file.close()
        
        # Create one record "BJ" in the file
        self.data_file="STATES_CP"
        self.data_file = File(self.data_file) 
        d1 = DynArray("")
        d1.insert(1, "北京")
        d1.insert(2, "北方")
        d1.insert(3, "亚洲")
        d1.insert(4, ["中国01","中国02"])
        d1.insert(5,["2015年5月28日","2014年5月28日"])
        self.data_file.write("BJ", d1)         

        self.create_test_file3("MEMBERS_CP")
        self.file_name = "MEMBERS_CP"
        self.field_id0 = "@ID"
        self.field_id1 = "ID"
        self.field_id2 = "NAME"
        self.field_id3 = "STATE_CODE"
        self.field_id4 = "STATE"
        self.field_id5 = "@"        
        
        self.dict_file = Dictionary(self.file_name)

        self.dict_file.set_type(self.field_id0, 'D')
        self.dict_file.set_loc(self.field_id0, 0)
        self.dict_file.set_conv(self.field_id0, '')
        self.dict_file.set_name(self.field_id0, '成员编号')
        self.dict_file.set_format(self.field_id0, '20L')
        self.dict_file.set_sm(self.field_id0, 'S')
        self.dict_file.set_assoc(self.field_id0, '')
        self.dict_file.set_sql_type(self.field_id0, '')

        self.dict_file.set_type(self.field_id1, 'D')
        self.dict_file.set_loc(self.field_id1, 0)
        self.dict_file.set_conv(self.field_id1, '')
        self.dict_file.set_name(self.field_id1, '成员编号')
        self.dict_file.set_format(self.field_id1, '20L')
        self.dict_file.set_sm(self.field_id1, 'S')
        self.dict_file.set_assoc(self.field_id1, '')

        self.dict_file.set_type(self.field_id2, 'D')
        self.dict_file.set_loc(self.field_id2, 1)
        self.dict_file.set_conv(self.field_id2, '')
        self.dict_file.set_name(self.field_id2, '成员名字')
        self.dict_file.set_format(self.field_id2, '20L')
        self.dict_file.set_sm(self.field_id2, 'S')
        self.dict_file.set_assoc(self.field_id2, '')

        self.dict_file.set_type(self.field_id3, 'D')
        self.dict_file.set_loc(self.field_id3, 2)
        self.dict_file.set_conv(self.field_id3, '')
        self.dict_file.set_name(self.field_id3, '州编号')
        self.dict_file.set_format(self.field_id3, '20L')
        self.dict_file.set_sm(self.field_id3, 'S')
        self.dict_file.set_assoc(self.field_id3, '')

        self.dict_file.set_type(self.field_id4, 'I')
        self.dict_file.set_loc(self.field_id4, "TRANS(STATES_CP,STATE_CODE,'NAME','C')")
        self.dict_file.set_conv(self.field_id4, '')
        self.dict_file.set_name(self.field_id4, '州名')
        self.dict_file.set_format(self.field_id4, '25L')
        self.dict_file.set_sm(self.field_id4, 'S')
        self.dict_file.set_assoc(self.field_id4, '')

        self.dict_file.set_type(self.field_id5, 'PH')
        self.dict_file.set_loc(self.field_id5, "ID NAME STATE_CODE")
        self.dict_file.set_conv(self.field_id5, '')
        self.dict_file.set_name(self.field_id5, '')
        self.dict_file.set_format(self.field_id5, '')
        self.dict_file.set_sm(self.field_id5, '')
        self.dict_file.set_assoc(self.field_id5, '')

        self.dict_file.close()
        
        # Create one record "张三" in the file
        mDataFile = File("MEMBERS_CP") 
        wrec = DynArray("")
        wrec.insert(1, "张三")
        wrec.insert(2, "BJ")
               
        mDataFile.write("001", wrec) 
                 
        mDataFile.close()        
        
    def tearDown(self):
        self.delete_test_file("STATES_CP")
        self.delete_test_file("MEMBERS_CP")
        super().tearDown()

    def test_DictWrite(self):
        # Define a DICT file object, add a field for it
        dictFile=Dictionary("STATES_CP")
        d1 = DynArray("")
        d1.insert(1, "D")
        d1.insert(2, '6')
        d1.insert(3, "")
        d1.insert(4, "字段6")
        d1.insert(5, "40L")
        d1.insert(6, "S")
        dictFile.write("字段6", d1)
        rec=dictFile.read("字段6")
        self.assertEqual(str(rec[0:6]), str(d1[0:6]))
        
        bCmd=Command("LIST DICT STATES_CP WITH LOC=6") 
        bCmd.run()  
        self.assertIn("字段6", bCmd.response)
         
        # Test add a "PH" type field
        d2 = DynArray("")
        d2.insert(1, "PH")
        d2.insert(2, "ID NAME")        
        dictFile.write("STATES_CPINFO", d2)  
        rec2 = dictFile.read("STATES_CPINFO")
        self.assertEqual(bytes(rec2), b'PH\xfeID NAME')
                                  
        bCmd2=Command("LIST DICT STATES_CP WITH @ID='STATES_CPINFO'") 
        bCmd2.run()  
        self.assertIn("PH", bCmd2.response)
         
        # Test the fieldid is null, the value is null
        dictFile.write("", "")
        rec3 = dictFile.read("")
        self.assertEqual(bytes(rec3), b'')  

        # Test write() method, not set any parameters for it
        self.assertRaises(TypeError, dictFile.write, )
                     
        # Test write() method, just set fieldid for it
        self.assertRaises(TypeError, dictFile.write, "STATES_CPINFO")
                                    
        # Delete the fields after test
        dictFile.delete("字段6")  
        dictFile.delete("STATES_CPINFO")
        dictFile.delete("")
        self.assertRaises(UOError, dictFile.read, "字段6") 
        self.assertRaises(UOError, dictFile.read, "STATES_CPINFO")  
        self.assertRaises(UOError, dictFile.read, "")

    def test_DictRead(self):                         
        # -----------------------Test DICT file--------------------
        # Define a DICT file object, read fields from it
        dictFile = Dictionary("MEMBERS_CP")
        rec = dictFile.read("ID")       
        self.assertEqual(str(rec[0]), "D")    
        self.assertEqual(str(rec[1]), "0") 
        self.assertEqual(str(rec[2]), "") 
        self.assertEqual(str(rec[3]), "成员编号") 
        self.assertEqual(str(rec[4]), "20L") 
        self.assertEqual(str(rec[5]), "S")  

        #Read "I" type field for UniVerse
        rec = dictFile.read("STATE")        
        self.assertEqual(str(rec[0]), "I")    
        self.assertEqual(str(rec[1]), "TRANS(STATES_CP,STATE_CODE,'NAME','C')") 
        self.assertEqual(str(rec[2]), "") 
        self.assertEqual(str(rec[3]), "州名") 
        self.assertEqual(str(rec[4]), "25L") 
        self.assertEqual(str(rec[5]), "S")  

        # Test read a field that doesn't exist       
        self.assertRaises(UOError, dictFile.read, "DD") 

        # Check the field lock 
        d1 = DynArray("")
        d1.insert(1, "D")
        d1.insert(2, "6")
        d1.insert(3, "")
        d1.insert(4, "字段6")
        d1.insert(5, "40L")
        d1.insert(6, "S")
        dictFile.write("字段6", d1) 
        rec = dictFile.read("字段6")
        self.assertEqual(str(rec[3]), str("字段6")) 

        dictFile.read("字段6", uopy.LOCK_EXCLUSIVE + uopy.LOCK_WAIT)

        bCmd=Command("LIST.READU") 
        bCmd.run()  
        self.assertIn("字段6", bCmd.response)
        self.assertIn("RU", bCmd.response)
        
        # Test not specify the parameter, mem.read()   
        # It will cause TypeError: function takes at least 1 argument (0 given)           
        self.assertRaises(TypeError, dictFile.read)

        # Test if the lock can be generated       
        dictFile.read("STATE_CODE", uopy.LOCK_EXCLUSIVE + uopy.LOCK_WAIT)
        result = dictFile.is_locked("STATE_CODE")
        self.assertEqual(result, True)        
        dictFile.unlock("STATE_CODE")  
        
        # Delete the field after test
        dictFile.delete("字段6")              
        dictFile.close() 

    def test_DictReadField(self): 
        dictFile = Dictionary("MEMBERS_CP")
          
        d1 = DynArray("")
        d1.insert(1, "D")
        d1.insert(2, "6")
        d1.insert(3, "")
        d1.insert(4, "字段6")
        d1.insert(5, "40L")
        d1.insert(6, "S")
        dictFile.write("字段6", d1) 
        rec = dictFile.read("字段6")
        self.assertEqual(str(rec[3]), str("字段6"))  
        rec = dictFile.read("字段6")
        self.assertEqual(str(rec[0:6]), str(d1[0:6]))

        rec = dictFile.read_field("字段6", 4)
        self.assertEqual(str(rec), str("字段6"))          

        rec = dictFile.read_field("STATE", 1)
        #print(bytes(rec))
        self.assertEqual(bytes(rec), b'I')  

        # Read "STATE" field's "NAME" column
        rec = dictFile.read_field("STATE", 4)
        self.assertEqual(str(rec), str("州名")) 

        # Read "LOCATION_ZIP" field's "SM" column
        rec = dictFile.read_field("NAME", 6)
        self.assertEqual(bytes(rec), b'S') 

        # Read "ID" field's "CONV" column                               
        rec = dictFile.read_field("ID", 3)
        self.assertEqual(bytes(rec), b'') 

        # Read "ID" field's column that bigger than it displayed
        rec = dictFile.read_field("ID", 100)
        self.assertEqual(bytes(rec), b'')   

        # Test read a not existing field 
        # It will cause UOError: Record not found 
        self.assertRaises(UOError, dictFile.read_field, "PID", 1)  

       # Test just specify one parameter, prod.readv(1)
        # It will cause TypeError: function takes at least 2 arguments (1 given)           
        self.assertRaises(TypeError, dictFile.read_field, 1)  

        # Delete the field after test
        dictFile.delete("字段6")              
        dictFile.close() 

    def test_DictWriteField(self): 
        # -----------------------Test DICT file--------------------  
        # Define a DICT file object, add a field for it
        dictFile=Dictionary("STATES_CP")

        d1 = DynArray("")
        d1.insert(1, "D")
        d1.insert(2, "6")
        d1.insert(3, "")
        d1.insert(4, "人口数量")
        d1.insert(5, "10L")
        d1.insert(6, "S")
        dictFile.write("人口数量", d1) 
        rec = dictFile.read("人口数量")
        self.assertEqual(str(rec[0:6]), str(d1[0:6]))

        # Using writev to update one attribute
        dictFile.write_field("人口数量", 5, "20L" )
        rec = dictFile.read_field("人口数量", 5)
        self.assertEqual(bytes(rec), b'20L') 

        dictFile.write_field("人口数量", 4, "")
        rec = dictFile.read_field("人口数量", 4)
        self.assertEqual(bytes(rec), b'')                          

        dictFile.write_field("人口数量", 1, "PH")
        rec = dictFile.read_field("人口数量", 1)
        self.assertEqual(bytes(rec), b'PH') 

        # Test just specify one parameter, dictFile.write_field("MANAGER")
        # It will cause TypeError: function takes at least 3 arguments (1 given)           
        self.assertRaises(TypeError, dictFile.write_field, "人口数量")  

        # Test the fieldnum is not an integer
        # It will cause TypeError: an integer is required(got type str)
        self.assertRaises(UOError, dictFile.write_field, "人口数量", "1", "PH")

        # Test the fieldnum is very large
        self.assertRaises(struct.error, dictFile.write_field, "人口数量", 1234567890123456789, "PH") 

        # Test the fieldid is null
        dictFile.write_field("", 1, "PH")
        rec = dictFile.read("")
        self.assertEqual(bytes(rec), b'PH')
        
        # Delete the field after test
        dictFile.delete("人口数量")
        dictFile.delete("")
        self.assertRaises(UOError, dictFile.read, "人口数量") 
        self.assertRaises(UOError, dictFile.read, "")   
        dictFile.close()  

    def test_DictDelete(self):           
        # -----------------------Test DICT file-------------------- 
        # Test delete a field that doesn't exist
        dictFile = Dictionary("STATES_CP")
        self.assertRaises(UOError, dictFile.delete, "UU") 

        # Test not specify any parameters
        self.assertRaises(TypeError, dictFile.delete)

        # Test specify more parameters for the method
        # It will cause UOError: function takes at most 2 arguments (3 given)
        self.assertRaises(TypeError, dictFile.delete, "ID", 1, uopy.LOCK_RETAIN) 

        d1 = DynArray("")
        d1.insert(1, "PH")
        d1.insert(2, "ID NAME")
        dictFile.write("州信息", d1) 
        rec = dictFile.read("州信息")
        self.assertEqual(str(rec[0:2]), str(d1[0:2]))
        
        dictFile.delete("州信息")
        self.assertRaises(UOError, dictFile.read, "州信息")
        dictFile.close() 

    def test_DictLockAndUnlock(self): 
        # -----------------------Test DICT file--------------------
        # Test lock a "PH" field
        dictFile = Dictionary("STATES_CP")
        d1 = DynArray("")
        d1.insert(1, "PH")
        d1.insert(2, "ID NAME")
        dictFile.write("州信息", d1)
        rec = dictFile.read("州信息")
        self.assertEqual(str(rec[0:2]), str(d1[0:2])) 

        dictFile.lock("州信息")
        result = dictFile.is_locked("州信息")
        self.assertEqual(result, True) 

        cmd=Command()       
        cmd.command_text = "LIST.READU" 
        cmd.run()
        self.assertIn("州信息",cmd.response) 
        self.assertIn("RU",cmd.response)

        # Unlock it and delete it
        dictFile.unlock("州信息")
        result = dictFile.is_locked("州信息")
        self.assertEqual(result, False)        
        dictFile.delete("州信息")
        self.assertRaises(UOError, dictFile.read, "州信息")
        dictFile.close()

        # lock a "I" type field 
        dictFile = Dictionary("MEMBERS_CP")   
        dictFile.lock("STATE")
        result = dictFile.is_locked("STATE")
        self.assertEqual(result, True) 

        cmd=Command()       
        cmd.command_text = "LIST.READU" 
        cmd.run()
        self.assertIn("STATE",cmd.response) 
        self.assertIn("RU",cmd.response)

        #Lock a field that doesn't exist, it should raise exception 
        self.assertRaises(UOError, dictFile.lock, "英文名")

        # Not specify any parameters    
        self.assertRaises(TypeError, dictFile.lock)  

        # Test unlock a field that doesn't exist
        # The result is no error occurs
        dictFile.unlock("距离")
        result = dictFile.is_locked("距离")
        self.assertEqual(result, False)

        # Test not specify any fields
        # It will clear all the locks on the file        
        dictFile.lock("ID")
        dictFile.lock("NAME")
        self.assertEqual(dictFile.is_locked("ID"), True)
        self.assertEqual(dictFile.is_locked("NAME"), True)        
                                
        dictFile.unlock("ID")
        dictFile.unlock("NAME")            
        self.assertEqual(dictFile.is_locked("ID"), False)
        self.assertEqual(dictFile.is_locked("NAME"), False)    
                
        dictFile.close() 

    def test_DictOpenAndClose(self):    
        # -----------------------Test DICT file--------------------
        dictFile = Dictionary("STATES_CP")
        dictFile.close()

        # Do write, read, lock, unlock, clear operations on a closed DICT file
        d1 = DynArray("")
        d1.insert(1, "D")
        d1.insert(2, "7")
        d1.insert(3, "")
        d1.insert(4, "字段5")
        d1.insert(5, "2L")
        d1.insert(6, "S")
                 
        self.assertRaises(TypeError, dictFile.write, d1)
        self.assertRaises(UOError, dictFile.write_field, "STATE", 1, "D") 
        self.assertRaises(UOError, dictFile.read, "STATE")                 
        self.assertRaises(UOError, dictFile.read_field, "NAME", 2)
        self.assertRaises(UOError, dictFile.lock, "ID")
        self.assertRaises(TypeError, dictFile.unlock)
        self.assertRaises(UOError, dictFile.clear)

        # Add an invalid parameter for the close() method
        # It will cause TypeError: close() takes no arguments (1 given)
        self.assertRaises(TypeError, dictFile.close, "STATES_CP")

        # Open the file
        dictFile.open()
                             
        rec = dictFile.read("ID")      
        self.assertEqual(str(rec[0]), str("D"))
        self.assertEqual(str(rec[1]), str("0"))
        self.assertEqual(str(rec[2]), str(""))
        self.assertEqual(str(rec[3]), str("州编号"))
        self.assertEqual(str(rec[4]), str("20L"))
        self.assertEqual(str(rec[5]), str("S"))
                             
        dictFile.close()

    def test_DictLockfileAndUnlockfile(self): 
        # -----------------------Test DICT file--------------------                                    
        dictFile = Dictionary("STATES_CP")
        dictFile.lock_file()
        # Test if the above lock is generated
        result = dictFile.is_locked("STATES_CP")
        self.assertEqual(result, True)

        # Unlock the file, specify a parameter for it
        # It will cause TypeError 
        self.assertRaises(TypeError, dictFile.unlock_file, "STATES_CP")  
                      
        # Unlock the file
        dictFile.unlock_file()      
        # Test if the above lock is unlocked
        result = dictFile.is_locked("STATES_CP")
        self.assertEqual(result, False)
                                
        # Lock the file, specify a parameter for it 
        # It will cause TypeError
        self.assertRaises(TypeError, dictFile.lock_file, "STATES_CP")
        dictFile.close() 

    def test_DictLockRelease(self):
        # -----------------------Test DICT file--------------------
        # Test the field lock can be released by the commands WRITE and DELETE issued from the same process
        dictFile = Dictionary("STATES_CP")
        field = DynArray("")
        field.insert(1, "PH")
        field.insert(2, "ID NAME")
        dictFile.write("州信息", field)
        rec = dictFile.read("州信息")
        self.assertEqual(rec[0:2], field[0:2])        

        dictFile.lock("州信息", uopy.LOCK_EXCLUSIVE)
        result = dictFile.is_locked("州信息")
        self.assertEqual(result, True)

        # The lock can not be released by read
        dictFile.read("州信息")
        result = dictFile.is_locked("州信息")
        self.assertEqual(result, True)
        
        # Can be released by write operation
        field = DynArray("")
        field.insert(1, "PH")
        field.insert(2, "ID STATE")
        dictFile.write("州信息", field)
        result = dictFile.is_locked("州信息")
        self.assertEqual(result, False)
 
         # Can be released by write_field operation
        dictFile.read("州信息", uopy.LOCK_EXCLUSIVE) 
        result = dictFile.is_locked("州信息")
        self.assertEqual(result, True)  
                             
        dictFile.write_field("州信息", 2, "ID NAME")
        result = dictFile.is_locked("州信息")
        self.assertEqual(result, False)                
                             
        # Can be released by delete operation
        # Using read() to lock the record firstly
        dictFile.read("州信息", uopy.LOCK_EXCLUSIVE)   
        result = dictFile.is_locked("州信息")
        self.assertEqual(result, True)  
                             
        dictFile.delete("州信息")
        result = dictFile.is_locked("州信息")
        self.assertEqual(result, False) 
        dictFile.close() 

    def test_DictLockCheckMulProcess(self):
        sysStr = platform.system()
        uhome = str(os.getenv("UVHOME"))
        pythonExec = str(sys.executable)
        cwd=str(os.getcwd())
        
        if (sysStr == "Windows"):
            p = subprocess.Popen(pythonExec+" -m unittest discover -s " + "." + os.sep + " -p uopy_dictfilelock_subprocess_cn.py", stdin=subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        else:
            p = subprocess.Popen(pythonExec + " -m unittest discover -s " + "." + os.sep + " -p uopy_dictfilelock_subprocess_cn.py", stdin=None, stdout = None, stderr = None, shell = True)            

        sleep(1)
        # Lock a field in the dict file.
        # Prepare the test condition for "test_LockCheckForMulProcess" method's test under "TestDictFileClass" class
        dictFile = Dictionary("STATES_CP") 

        # Check if the field is locked by subprocess
        result = dictFile.is_locked("dict测试")
        self.assertEqual(result, True) 

        # Delete the field
        # It will cause u2py.U2Error: file or record is locked by another user
        self.assertRaises(UOError, dictFile.delete, "dict测试")   

        # Update the record
        # It will cause UOError: file or record is locked by another user   
        self.assertRaises(UOError, dictFile.write_field, "dict测试", 5, "20L") 

        # Read the record
        rec = dictFile.read("dict测试")
        self.assertEqual(str(rec[0]), str("D"))
        self.assertEqual(str(rec[1]), str("9"))
        self.assertEqual(str(rec[2]), str(""))
        self.assertEqual(str(rec[3]), str("dict测试"))
        self.assertEqual(str(rec[4]), str("40L"))
        self.assertEqual(str(rec[5]), str("S"))

        # Try to lock the record that has been locked by another user 
        # It will cause UOError: file or record is locked by another user         
        self.assertRaises(UOError, dictFile.lock, "dict测试")  

        # Try to lock the file
        # It will cause UOError: file or record is locked by another user        
        self.assertRaises(UOError, dictFile.lock_file)

        # After this wait time, the subprocess run will complete, the lock will be released 
        p.terminate()    
        p.wait(3)               
        result = dictFile.is_locked("dict测试")
        self.assertEqual(result, False)
        dictFile.delete("dict测试")
        dictFile.close()

    def test_DataWrite(self):
        #-------------Test data file-----------------------      
        # Test write() method, contains single value and MV value
        # Write a record into the file and read it
        dataFile = File("STATES_CP")
        d1 = DynArray("")
        d1.insert(1, "纽约")
        d1.insert(2, "Northeast东北")
        d1.insert(3, "%大西洋中部%")
        d1.insert(4, ["美国01", "美国02"])
        d1.insert(5, ["2015年5月28日", "2014年5月28日"])
        dataFile.write("NY测试", d1) 
        
        rec = dataFile.read("NY测试", uopy.LOCK_EXCLUSIVE+uopy.LOCK_WAIT)
        self.assertEqual(str(d1[0:5]), str(rec[0:5]))

        cmd=Command()       
        cmd.command_text = "LIST.READU" 
        cmd.run()
        self.assertIn("NY测试",cmd.response)
        
        # Use islocked() method to test if the record is locked       
        result = dataFile.is_locked("NY测试")
        self.assertEqual(result, True) 

        # Test write a same record in the file         
        dataFile.unlock("NY测试")
        dataFile.write("NY测试", d1)
        rec = dataFile.read("NY测试")
        self.assertEqual(str(d1[0:5]), str(rec[0:5]))

        # Test write a record that have the same ID in the file         
        dataFile.unlock("NY测试")
        d1[3] = "中国"
        d1[4] = "2016年5月28日"
        dataFile.write("NY测试", d1) 
        rec = dataFile.read("NY测试")
        self.assertEqual(str(d1[0:5]), str(rec[0:5]))

        # Try to write a MV value into a single type field(SM = S): REGION
        d1[1]=["Northeast", "东北"]
        dataFile.write("NY测试", d1)        
        rec = dataFile.read("NY测试")
        self.assertEqual(str(d1[0:5]), str(rec[0:5]))

        cmd=Command()       
        cmd.command_text = "LIST STATES_CP WITH ID='NY测试'" 
        cmd.run()
        self.assertIn("Northeast",cmd.response)
        self.assertIn("东北",cmd.response)

        # Test the recordid is null, the value is null
        dataFile.write("", "")
        rec = dataFile.read("")
        self.assertEqual(bytes(rec), b'') 

        # Test write() method, not set any parameters for it
        self.assertRaises(TypeError, dataFile.write, )

        # Test write() method, just set recordid for it
        self.assertRaises(TypeError, dataFile.write, "NY测试")

        # Delete the record after test
        dataFile.delete("NY测试")
        self.assertRaises(UOError, dataFile.read, "NY测试") 
        dataFile.delete("")
        self.assertRaises(UOError, dataFile.read, "")           
        dataFile.close()
        
    def test_DataRead(self):
        # -----------------------Test data file--------------------                                     
        # Test read an existing record from the file
        dataFile = File("STATES_CP")  
        rec = dataFile.read("BJ")
        self.assertEqual(str(rec[0]), str("北京"))
        self.assertEqual(str(rec[1]), str("北方"))
        self.assertEqual(str(rec[2]), str("亚洲"))
        self.assertEqual(str(rec[3]), str(["中国01","中国02"]))
        self.assertEqual(str(rec[4]), str(["2015年5月28日","2014年5月28日"]))

        # Test read a record that doesn't exist
        # It will cause UOError: Record not found 
        self.assertRaises(UOError, dataFile.read, "EE")  
                     
        # Test the record id is empty
        # It will cause UOError: Record not found 
        self.assertRaises(UOError, dataFile.read, "")                                    
                           
        # Test not specify the parameter, dataFile.read()   
        # It will cause TypeError: function takes at least 1 argument (0 given)           
        self.assertRaises(TypeError, dataFile.read)

        # Specify a valid lock, test if the lock can be generated       
        dataFile.read("BJ", uopy.LOCK_EXCLUSIVE + uopy.LOCK_WAIT)
        result = dataFile.is_locked("BJ")
        self.assertEqual(result, True)        
        dataFile.unlock("BJ")          
        dataFile.close() 
                        
    def test_DataReadnamedfields(self):
        # -----------------------Test data file-------------------- 
        # Check read "mv" type field: AMENDED_BY from STATES_CP file
        dataFile = File("STATES_CP")
        d = DynArray()
        d.insert(1, "NAME")
        d.insert(2, "AMENDED_BY")     
        rec = dataFile.read_named_fields("BJ", d)
        recList=rec[3]  
        self.assertEqual(str(recList[0][0]), str("北京"))
        self.assertEqual(str(recList[0][1]), str(["中国01","中国02"]))

        # Test specify a field "ZZ" that doesn't exist
        d[1]="ZZ"
        rec = dataFile.read_named_fields("BJ", d)
        recList=rec[3]        
        self.assertEqual(str(recList[0][0]), str("北京"))
        self.assertEqual(str(recList[0][1]), str("BJ"))  
                
        # Test the record id is empty
        # It will cause UOError: Record not found 
#         self.assertRaises(UOError, dataFile.read_named_fields, "", d) 

        # Test the u2py.DynArray is empty, it means not specify any fields name
        # The result is that it will cause u2py.U2Error: No field name specified
#         d1 = DynArray()
#         self.assertRaises(UOError, dataFile.read_named_fields, "BJ", d1)

        # Specify a valid lock, test if the lock can be generated  
        d2 = DynArray()
        d2.insert(1, "NAME")
        d2.insert(2, "AMENDED_BY") 
        rec1 = dataFile.read_named_fields("BJ", d2, uopy.LOCK_EXCLUSIVE + uopy.LOCK_WAIT)
        result = dataFile.is_locked("BJ")
        self.assertEqual(result, True)        
        dataFile.unlock("BJ") 
        
        dataFile.close()

    def test_DataReadField(self):
        # -----------------------Test data file--------------------                                                      
        # Test read_field() method 
        # Test read the specified fields ((test single value))
        sts = File("STATES_CP") 
        nameField = sts.read_field("BJ", 1)
        self.assertEqual(str(nameField), str("北京")) 

        nameField = sts.read_field("BJ", 2)
        self.assertEqual(str(nameField), str("北方"))

        # Read the AMENDED_BY field (test MV value) 
        d=DynArray()
        d.insert(1, "中国01")
        d.insert(2, "中国02")                
        rec = sts.read_field("BJ", 4)
        self.assertEqual((str(rec)), str(d))

        # Test read a not existing field
        nameField = sts.read_field("BJ", 20)
        self.assertEqual(bytes(nameField), b'')  

        # Test read a not existing record 
        # It will cause u2py.U2Error: Record not found 
        self.assertRaises(UOError, sts.read_field, "AI", 1)    

        # Test just specify one parameter, sts.readv(1)
        # It will cause TypeError: function takes at least 2 arguments (1 given)           
        self.assertRaises(TypeError, sts.read_field, 1)

        # Test the record id is empty
        # It will cause u2py.U2Error: Record not found 
        self.assertRaises(UOError, sts.read_field, "", 1)  

        # Specify a valid lock, test if the lock can be generated       
        rec= sts.read_field("BJ", 1, uopy.LOCK_SHARED + uopy.LOCK_WAIT)
        self.assertEqual(str(rec), str("北京"))         
        result = sts.is_locked("BJ")
        self.assertEqual(result, True)        
        sts.unlock("BJ")   

        # Test read data from MEMBERS_CP file
        # Read id field
        mem = File("MEMBERS_CP")
        nameField = mem.read_field("001", 0)
        self.assertEqual(bytes(nameField), b'001')

        # Read NAME field
        nameField = mem.read_field("001", 1)
        self.assertEqual(str(nameField), str("张三"))    

        sts.close()
        mem.close() 

    def test_DataWriteField(self): 
        # -----------------------Test data file--------------------       
        # Test writev(), the recordid doesn't exist in the file
        # It will write a new record into the file
        sts = File("STATES_CP")
        sts.write_field("SH", 1, "上海")
        rec = sts.read("SH")
        self.assertEqual(str(rec), str("上海"))  

        # Test writev() method, the recordid exists in the file        
        sts.write_field("SH", 2, "北方")
        rec = sts.read("SH")
        self.assertEqual(str(rec[0]), str("上海"))
        self.assertEqual(str(rec[1]), str("北方")) 

        # Test write MV value
        wrec = DynArray("")
        wrec.insert(1, ["中国01", "中国02"])
        sts.write_field("SH", 4, wrec)
        rec = sts.read("SH")
        self.assertEqual(str(rec[0]), str("上海"))
        self.assertEqual(str(rec[1]), str("北方"))
        self.assertEqual(str(rec[2]), str(""))
        self.assertEqual(str(rec[3][0]), str("中国01"))       
        self.assertEqual(str(rec[3][1]), str("中国02"))

        # Test just specify one parameter, sts.writev("AA")
        # It will cause TypeError: function takes at least 3 arguments (1 given)           
        self.assertRaises(TypeError, sts.write_field, "AA")

        # Test specify a fieldnum that bigger than the file's defined fieldnum
        # It will write the field value into the specified fieldnum 6
        sts.write_field("SY", 6, "北方")
        rec = sts.read("SY")
#         print(str(rec))
        self.assertEqual(str(rec[0]), str(""))     
        self.assertEqual(str(rec[5]), str("北方"))  

        # Test the recordid is null
        sts.write_field("", 1, "测试")
        rec = sts.read("")
        self.assertEqual(str(rec), str("测试"))

        # Delete the records after test
        sts.delete("SH")
        self.assertRaises(UOError, sts.read, "SH")
        sts.delete("")
        self.assertRaises(UOError, sts.read, "")                           
        sts.close() 

    def test_DataWritenamedfields(self):
        # -----------------------Test data file--------------------
        # Write specified values for specified fields into STATES_CP 
        # The record id doesn't exist in the file
        # d1 is used for fields name, d2 is used for values
        sts = File("STATES_CP")
        recordID=["DL", "SZ"]
        d1=["NAME", "REGION", "AMENDED_BY"]        
        d2=[["大连", "北方", ["辽宁", "吉林"]],["苏州", "南方", ["江苏", "浙江"]]]     
                        
        sts.write_named_fields(recordID, d1, d2)
        rec = sts.read("DL")
        self.assertEqual(str(rec[0]), str("大连"))
        self.assertEqual(str(rec[1]), str("北方"))
        self.assertEqual(str(rec[2]), "")
        self.assertEqual(str(rec[3]), str(["辽宁", "吉林"]))

        # Test just specify one parameter for the method
        self.assertRaises(TypeError, sts.write_named_fields, "DL") 

        # Delete the record after test
        sts.delete("DL")
        self.assertRaises(UOError, sts.read, "DL") 
                           
        sts.close()

    def test_DataDelete(self): 
        # -----------------------Test data file--------------------                             
        # Test delete a record that doesn't exist
        sts = File("STATES_CP")
        self.assertRaises(UOError, sts.delete, "CN")  

        # Test not specify any parameters
        self.assertRaises(TypeError, sts.delete)

        # Test specify an invalid lock
        # It will cause u2py.U2Error: lock flag must be either 0, LOCK_RETAIN, LOCK_RETAIN + LOCK_WAIT
        self.assertRaises(UOError, sts.delete, "AL", uopy.LOCK_EXCLUSIVE)

        # Test specify more parameters for the method
        # It will cause TypeError: function takes at most 2 arguments (3 given)
        self.assertRaises(TypeError, sts.delete, "AL", 1, uopy.LOCK_RETAIN) 

        # Delete a record
        sts.write("DL", "大连")
        rec = sts.read("DL")
        self.assertEqual(str(rec), str("大连"))  
        sts.delete("DL")
                          
        # Check if the record has been deleted
        self.assertRaises(UOError, sts.read, "DL")
        sts.close() 

    def test_DataLockAndUnlock(self): 
        # -----------------------Test data file--------------------        
        # Test lock() method, not specify the lock type
        # It locked the LOCK_EXCLUSIVE lock as default (M = X)
  
        sts = File("STATES_CP")        
        sts.lock("BJ")
        result = sts.is_locked("BJ")
        self.assertEqual(result, True)  

        cmd=Command()       
        cmd.command_text = "LIST.READU" 
        cmd.run()
        self.assertIn("BJ",cmd.response) 
        self.assertIn("RU",cmd.response)

        # Change the LOCK_EXCLUSIVE lock to LOCK_SHARED
        # The result is that the lock type can not be changed
        sts.lock("BJ", uopy.LOCK_SHARED)

        cmd=Command()       
        cmd.command_text = "LIST.READU" 
        cmd.run()
        self.assertIn("BJ",cmd.response) 
        self.assertIn("RU",cmd.response)
        
        # unlock the lock and lock it as LOCK_SHARED (M = S)
        sts.unlock("BJ")
        result = sts.is_locked("BJ")
        self.assertEqual(result, False) 
           
        sts.lock("BJ", uopy.LOCK_SHARED)
        cmd=Command()       
        cmd.command_text = "LIST.READU" 
        cmd.run()
        self.assertIn("BJ",cmd.response) 
        self.assertIn("RL",cmd.response)

        # Change the LOCK_SHARED lock to LOCK_EXCLUSIVE
        # It will be successful, can be changed
        sts.lock("BJ", uopy.LOCK_EXCLUSIVE)
        sts.lock("BJ", uopy.LOCK_SHARED)
        cmd=Command()       
        cmd.command_text = "LIST.READU" 
        cmd.run()
        self.assertIn("BJ",cmd.response) 
        self.assertIn("RU",cmd.response)
        sts.unlock("BJ")
        
        # Not specify any parameters    
        self.assertRaises(TypeError, sts.lock)    
           
        # Test not specify any recordids
        # It will clear all the locks on the file        
        sts.lock("BJ")
        self.assertEqual(sts.is_locked("BJ"), True)
                             
        sts.unlock("BJ")
                          
        self.assertEqual(sts.is_locked("BJ"), False)
        sts.close()

    def test_DataOpenAndClose(self):
        # -----------------------Test data file--------------------                                     
        # Close the sts object
        sts = File("STATES_CP")
        sts.close()

        # Do write, read, lock, unlock, clear operations on a closed file
        self.assertRaises(UOError, sts.write, "SY", "沈阳")
        self.assertRaises(UOError, sts.write_field, "SY", 1, "沈阳") 
        self.assertRaises(UOError, sts.read, "BJ")                 
        self.assertRaises(UOError, sts.read_field, "BJ", 2)
        self.assertRaises(UOError, sts.lock, "BJ")
        self.assertRaises(TypeError, sts.unlock)
        self.assertRaises(UOError, sts.clear) 

        # Add an invalid parameter for the close() method
        # It will cause TypeError: close() takes no arguments (1 given)
        self.assertRaises(TypeError, sts.close, "STATES_CP")        

        # Open the file
        sts.open()
                          
        sts.write("SY", "沈阳")
        rec = sts.read("SY")
        self.assertEqual(str(rec), str("沈阳"))
                          
        sts.lock("SY")
        result = sts.is_locked("SY")
        self.assertEqual(result, True)
        sts.unlock("SY")

        # Add an invalid parameter for the open() method
        # It will cause TypeError: open() takes no arguments (1 given)
        self.assertRaises(TypeError, sts.open, "STATES_CP")  

        # Delete the records after test
        sts.delete("SY")
        self.assertRaises(UOError, sts.read, "SY")
        sts.close()

    def test_DataLockfileAndUnlockfile(self):
        # -----------------------Test data file--------------------                                       
        sts = File("STATES_CP")
        sts.lock_file()
        # Test if the above lock is generated
        result = sts.is_locked("STATES_CP")
        self.assertEqual(result, True)

        # Unlock the file, specify a parameter for it
        # It will cause TypeError 
        self.assertRaises(TypeError, sts.unlock_file, "STATES_CP")

        # Unlock the file
        sts.unlock_file()      
        # Test if the above lock is unlocked
        result = sts.is_locked("STATES_CP")
        self.assertEqual(result, False)

        # Lock the file, specify a parameter for it 
        # It will cause TypeError
        self.assertRaises(TypeError, sts.lock_file, "STATES_CP")
        sts.close() 

    def test_DataLockRelease(self):
        # -----------------------Test data file--------------------                                           
        # Test the record lock can be released by the commands WRITE and DELETE issued from the same process
        sts = File("STATES_CP")
        sts.write("HF", "合肥")
        sts.lock("HF", uopy.LOCK_EXCLUSIVE)
        result = sts.is_locked("HF")
        self.assertEqual(result, True)

        # The lock can not be released by read
        sts.read("HF")
        result = sts.is_locked("HF")
        self.assertEqual(result, True)
                
        # Can be released by write operation
        wrec = DynArray("")
        wrec.insert(1, "合肥")
        wrec.insert(2, "South南方")
        wrec.insert(3, "亚洲")
        wrec.insert(4, "安徽")
        wrec.insert(5, "2015年5月28日")     
               
        sts.write("HF", wrec) 
        result = sts.is_locked("HF")
        self.assertEqual(result, False) 

        # Can be released by writev operation
        sts.write_field("DL", 1, "大连") 
                         
        sts.read("DL", uopy.LOCK_EXCLUSIVE + uopy.LOCK_WAIT) 
        result = sts.is_locked("DL")
        self.assertEqual(result, True)  
                         
        sts.write_field("DL", 1, "DALIAN大连")
        result = sts.is_locked("DL")
        self.assertEqual(result, False) 

        # Can be released by delete operation
        # Using read() to lock the record firstly
        sts.read("DL", uopy.LOCK_EXCLUSIVE + uopy.LOCK_WAIT)   
        result = sts.is_locked("DL")
        self.assertEqual(result, True)  
                         
        sts.delete("DL")
        result = sts.is_locked("DL")
        self.assertEqual(result, False) 

        # Test the lock can be released by writenamedfields operation
        sts.write("HF", "合肥")
        sts.lock("HF", uopy.LOCK_EXCLUSIVE)
        result = sts.is_locked("HF")
        self.assertEqual(result, True) 
                   
        recordID=["HF", "CC"]
        D1 = ["NAME", "REGION"]
        D2 = [["合肥", "south南方"],["长春", "north北方"]]
        sts.write_named_fields(recordID, D1, D2)
        result = sts.is_locked("HF")
        self.assertEqual(result, False) 
        sts.delete("HF")
        sts.close() 

    def test_DataLockCheckForMulProcess(self): 
        # -----------------------Test data file--------------------
        # Lock check for record under multiple process           
        # Test do some operations on a record which has been locked by another process
        sts = File("STATES_CP")
        sysStr = platform.system()        
        pythonExec = str(sys.executable)

        if (sysStr == "Windows"):
            p = subprocess.Popen(pythonExec+" -m unittest discover -s " + "." + os.sep + " -p uopy_datafilelock_subprocess_cn.py", stdin=subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        else:
            p = subprocess.Popen(pythonExec + " -m unittest discover -s " + "." + os.sep + " -p uopy_datafilelock_subprocess_cn.py", stdin=None, stdout = None, stderr = None, shell = True)            

        sleep(1)

        # Check if the record is locked by subprocess
        result = sts.is_locked("BJ")
        self.assertEqual(result, True)   

        # Delete the record
        # It will cause u2py.U2Error: file or record is locked by another user
        self.assertRaises(UOError, sts.delete, "BJ")   

        # Update the record
        # It will cause u2py.U2Error: file or record is locked by another user        
        self.assertRaises(UOError, sts.write, "BJ", "beijing北京") 

        # Read the record
        rec = sts.read("BJ")
        self.assertEqual(str(rec[0]), str("北京"))
        self.assertEqual(str(rec[1]), str("北方"))
        self.assertEqual(str(rec[2]), str("亚洲"))
        self.assertEqual(str(rec[3]), str(["中国01","中国02"]))
        self.assertEqual(str(rec[4]), str(["2015年5月28日","2014年5月28日"]))

        # Try to lock the record that has been locked by another user 
        # It will cause u2py.U2Error: file or record is locked by another user         
        self.assertRaises(UOError, sts.lock, "BJ")   

        # Try to lock the file
        # It will cause u2py.U2Error: file or record is locked by another user        
        self.assertRaises(UOError, sts.lock_file)
                             
        # After this wait time, the subprocess run will complete, the lock will be released 
        p.terminate()     
        p.wait(3)               
        result = sts.is_locked("BJ")
        self.assertEqual(result, False)
        sts.close()  
                                                                                            
if __name__ == '__main__':
    unittest.main()
