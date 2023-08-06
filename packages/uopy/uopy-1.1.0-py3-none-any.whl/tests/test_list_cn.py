# coding=utf-8

from uopy import UOError, EXEC_MORE_OUTPUT, List, Command, Dictionary, File, DynArray, Subroutine
from tests.unitestbase_cn import *
import os


class TestListCn(UniTestBaseCn):
    
    session = None

    def setUp(self):
        super().setUp()
        self.create_test_file30('CITY')
        self.file_name = "CITY"
        self.field_id1 = "PROVINCE_ID"
        self.field_id2 = "PROVINCE_NAME"
        self.field_id3 = "CITY_NAME"
        self.field_id4 = "DISTRICT_NAME"
        self.field_id5 = "P_SHORT"
        self.field_id6 = "PNAME_SHORT"
        self.field_id7 = "@SELECT"
        self.field_id8 = "@"

        self.dict_file = Dictionary(self.file_name)

        self.dict_file.set_type(self.field_id1, 'D')
        self.dict_file.set_loc(self.field_id1, 1)
        self.dict_file.set_conv(self.field_id1, '')
        self.dict_file.set_name(self.field_id1, 'Province ID')
        self.dict_file.set_format(self.field_id1, '20L')
        self.dict_file.set_sm(self.field_id1, 'S')
        self.dict_file.set_assoc(self.field_id1, '')
        self.dict_file.set_sql_type(self.field_id1, '')

        self.dict_file.set_type(self.field_id2, 'D')
        self.dict_file.set_loc(self.field_id2, 2)
        self.dict_file.set_conv(self.field_id2, '')
        self.dict_file.set_name(self.field_id2, 'Province Name')
        self.dict_file.set_format(self.field_id2, '20L')
        self.dict_file.set_sm(self.field_id2, 'S')
        self.dict_file.set_assoc(self.field_id2, '')
        self.dict_file.set_sql_type(self.field_id2, '')

        self.dict_file.set_type(self.field_id3, 'D')
        self.dict_file.set_loc(self.field_id3, 3)
        self.dict_file.set_conv(self.field_id3, '')
        self.dict_file.set_name(self.field_id3, 'City Name')
        self.dict_file.set_format(self.field_id3, '20L')
        self.dict_file.set_sm(self.field_id3, 'S')
        self.dict_file.set_assoc(self.field_id3, '')
        self.dict_file.set_sql_type(self.field_id3, '')

        self.dict_file.set_type(self.field_id4, 'D')
        self.dict_file.set_loc(self.field_id4, 4)
        self.dict_file.set_conv(self.field_id4, '')
        self.dict_file.set_name(self.field_id4, 'District Name')
        self.dict_file.set_format(self.field_id4, '20L')
        self.dict_file.set_sm(self.field_id4, 'M')
        self.dict_file.set_assoc(self.field_id4, '')
        self.dict_file.set_sql_type(self.field_id4, '')

        self.dict_file.set_type(self.field_id5, 'D')
        self.dict_file.set_loc(self.field_id5, 5)
        self.dict_file.set_conv(self.field_id5, '')
        self.dict_file.set_name(self.field_id5, 'Short Province Name')
        self.dict_file.set_format(self.field_id5, '20L')
        self.dict_file.set_sm(self.field_id5, 'S')
        self.dict_file.set_assoc(self.field_id5, '')
        self.dict_file.set_sql_type(self.field_id5, '')

        self.dict_file.set_type(self.field_id6, 'I')
        self.dict_file.set_loc(self.field_id6, 'PROVINCE_NAME:P_SHORT')
        self.dict_file.set_conv(self.field_id6, '')
        self.dict_file.set_name(self.field_id6, 'Province Short')
        self.dict_file.set_format(self.field_id6, '20L')
        self.dict_file.set_sm(self.field_id6, 'M')
        self.dict_file.set_assoc(self.field_id6, '')
        self.dict_file.set_sql_type(self.field_id6, '')

        self.dict_file.set_type(self.field_id7, 'PH')
        self.dict_file.set_loc(self.field_id7, 'PROVINCE_ID PROVINCE_NAME CITY_NAME DISTRICT_NAME')
        self.dict_file.set_conv(self.field_id7, '')
        self.dict_file.set_name(self.field_id7, '')
        self.dict_file.set_format(self.field_id7, '')
        self.dict_file.set_sm(self.field_id7, '')
        self.dict_file.set_assoc(self.field_id7, '')
        self.dict_file.set_sql_type(self.field_id7, '')

        self.dict_file.set_type(self.field_id8, 'PH')
        self.dict_file.set_loc(self.field_id8, 'PROVINCE_NAME CITY_NAME DISTRICT_NAME')
        self.dict_file.set_conv(self.field_id8, '')
        self.dict_file.set_name(self.field_id8, '')
        self.dict_file.set_format(self.field_id8, '')
        self.dict_file.set_sm(self.field_id8, '')
        self.dict_file.set_assoc(self.field_id8, '')
        self.dict_file.set_sql_type(self.field_id8, '')

        self.dict_file.close()

        self.data_file = File(self.file_name)
        
        recId = ["1", "2", "第3条"]
        d1 = [self.field_id1, self.field_id2, self.field_id3, self.field_id4, self.field_id5]
        
        d2 = ([["1", "辽宁", ["沈阳", "大连", "鞍山"], [["铁西区", "皇姑区"], ["中山区", "甘井子区", "沙河口区"], ["千山区", "立山区"]], "辽"],
             ["2", "河北", ["石家庄", "承德", "唐山"], [["新华区", "桥西区", "裕华区"], ["双桥区", "双滦区"], ["丰南区", "开平区"]]],
             ["The Third 记录", "山东", ["济南", "青岛"], [["历城区", "历下区"], ["崂山区", "李沧区"]], "鲁"]])   
            
        self.data_file.write_named_fields(recId, d1, d2)
            
        self.data_file.close()        
        
    def tearDown(self):
        self.delete_test_file("CITY")

        super().tearDown()

    def test_load_list_from_saved_list(self):
               
        # step1 Create a saved list        
        c1 = Command("SELECT CITY WITH PROVINCE_NAME = '河北'")
        c1.run()
        
        # step2 load the saved list to u2py.List
        l1 = List(0)
        # step3 read u2py.List to u2py.DynArray
        a = l1.read_list()
        self.assertEqual(str(a[0]), str("2"))
        
        self.assertRaises(UOError, List, 11)

        self.assertRaises(UOError, List, -1)
        self.assertRaises(UOError, List, 1236985)  

        # Create a saved list        
        c1 = Command("SELECT CITY WITH PROVINCE_NAME = '辽宁' OR PROVINCE_NAME = '山东' BY PROVINCE_ID")
        c1.run()
                              
        # load the saved list to List
        l1 = List(0)
                              
        # read List to DynArray
        a = l1.read_list()
                              
        # check if the excepted record ID is in the DynArray
        self.assertEqual(str(a[0]), str("1"))
        self.assertEqual(str(a[1]), str("第3条"))
        
        self.assertRaises(UOError, List, 11, "LN_SD")

        self.assertRaises(UOError, List, -1, "LN_SD")
        self.assertRaises(UOError, List, 1236985, "LN_SD")

        # test condition: virtual field
        c1 = Command("SELECT CITY WITH PNAME_SHORT = '山东鲁'")
        c1.run()
                   
        l = List(0)
                              
        # read List to DynArray
        a = l.read_list()
                              
        # check if the excepted record ID is in the DynArray 
        self.assertEqual(str(a[0]), str("第3条"))

    def test_chinese_file_name(self):
         
        c1 = Command("SELECT CITY WITH PROVINCE_NAME = '辽宁' OR PROVINCE_NAME = '山东' BY PROVINCE_ID")
        c1.run()
                               
        # load the saved list to List
        l1 = List(0)
                               
        # read List to DynArray
        a = l1.read_list()
                               
        # check if the excepted record ID is in the DynArray
        self.assertEqual(str(a[0]), str("1"))
        self.assertEqual(str(a[1]), str("第3条"))

    def test_load_list_from_file(self):
        
        rl = ["1", "2", "第3条"]        
        # open a file
        f = File("CITY")
                             
        # load the record ID of the file to List
        l = List(0).select(f)
        f.close()
        # step3 read List to DynArray
        
        i = 0                            
        # check if the excepted record ID is in the DynArray
        for recId in l:
            self.assertEqual(str(recId), str(rl[i]))
            i += 1
                                     
        # test condition:file is closed
        self.assertRaises(UOError, List(0).select, f)       

    def test_load_list_from_file_index(self):
                       
        # create index on a file
        c0 = Command("DELETE.INDEX CITY DISTRICT_NAME")
        c1 = Command("CREATE.INDEX CITY DISTRICT_NAME")
        c2 = Command("BUILD.INDEX CITY DISTRICT_NAME")
        c0.run()
        c1.run()
        c2.run()
                                   
        # open the file
        f = File("CITY")
                
        # Test TypeError
        self.assertRaises(TypeError, List(0).select_alternate_key, f, "DISTRICT_NAME", "新华区")
                               
        # load the record ID of the file to List via the index of the file
#         l = List(4,f,"DISTRICT_NAME","新华区")
        l = List(4).select_alternate_key(f, "DISTRICT_NAME")
        f.close()
        # step4 read List to DynArray
        a = l.read_list()
        # check if the excepted record ID is in the DynArray
        self.assertEqual(str(a[0]), str("中山区"))
                               
        # test condition: file is closed
        self.assertRaises(UOError, List(0).select_alternate_key, f, "DISTRICT_NAME")
        # test condition: index does not exist
        self.assertRaises(UOError, List(0).select_alternate_key, f, "DISTRICT_NAM")

    def test_list_clear(self):
        
        # step1 Create a saved list
        c1 = Command("SELECT CITY WITH PROVINCE_ID = 'The Third 记录'")
        c1.run()
                                 
        # step2 load the saved list to List
        l = List(0)
                                 
        # step3 read List to DynArray
        a = l.read_list()
                                 
        # step4 make sure the excepted record ID is in the DynArray
        self.assertEqual(str(a[0]), str("第3条"))
                             
        # step5 test double clear the list and print the content
        l.clear()
        a1 = l.read_list()
        
        self.assertEqual(a1, DynArray())

    def test_list_next(self):
                   
        # step1 Create a saved list
        c1 = Command("SELECT CITY WITH PROVINCE_ID = '1' OR PROVINCE_ID = 'The Third 记录' BY PROVINCE_ID")
        c1.run()
        # step2 load the saved list to List
        l = List(0)
        # step3 read List to DynArray
        a = l.next()  
                                  
        # step4 check the first record ID is in the DynArray
        self.assertEqual(a, DynArray("1"))
                              
        # step5 check the second record ID is in the DynArray 
        a1 = l.next()
        
        self.assertEqual(a1, DynArray("第3条"))
         
        # test next() method if there is no next value in the list
        a2 = l.next() 
        self.assertEqual(a2, DynArray())
       
    def test_list_read_list(self):
        # step1 Create a saved list
        c1 = Command("SELECT CITY WITH PROVINCE_ID = '1' OR PROVINCE_ID = 'The Third 记录' BY PROVINCE_ID")
        c1.run()
                              
        # step2 load the saved list to List
        l = List(0)
                                    
        # step3 read List to DynArray
        a = l.read_list() 
        self.assertEqual(str(a[0]), str("1"))
        self.assertEqual(str(a[1]), str("第3条"))
                              
        l.clear()
        a1 = l.read_list()
        self.assertEqual(a1, DynArray())
        
    def test_select_matching_ak(self):
               
        # create index on a file
        c0 = Command("DELETE.INDEX CITY DISTRICT_NAME")
        c1 = Command("CREATE.INDEX CITY DISTRICT_NAME")
        c2 = Command("BUILD.INDEX CITY DISTRICT_NAME")
        c0.run()
        c1.run()
        c2.run()
                                   
        # open the file
        f = File("CITY")

        # Test TypeError
        self.assertRaises(UOError, List(4).select_matching_ak, "CITY", "DISTRICT_NAME", "新华区")
                
        # load the record ID of the file to List via the index of the file
        l = List(4).select_matching_ak(f,"DISTRICT_NAME","新华区")

        f.close()
        # step4 read List to DynArray
        a = l.read_list()
        # check if the excepted record ID is in the DynArray
        self.assertEqual(str(a[0]), str("2"))
                
        # test condition: file is closed
        self.assertRaises(UOError, List(0).select_matching_ak, f, "DISTRICT_NAME", "新华区")
        # test condition: index does not exist
        self.assertRaises(UOError, List(0).select_matching_ak, f, "DISTRICT_NAM", "新华区")

                                        
if __name__ == '__main__':
    unittest.main()
