# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

from uopy import UOError, EXEC_MORE_OUTPUT, SequentialFile, Command, Dictionary, File, DynArray, Subroutine
from tests.unitestbase_cn import *
import os

class TestCommandCn(UniTestBaseCn):
    session = None

    def setUp(self):
        super().setUp()
        self.create_test_file3('MOVIEScp')
        self.create_test_file3('MOVIES')
        self.file_name = "MOVIES"
        self.field_id0 = "@ID"
        self.field_id1 = "COUNTRY"
        self.field_id2 = "MOVIENAME"
        self.field_id3 = "ACTRESS"
        self.field_id4 = "ACTOR"
        self.field_id5 = "BOXOFFICE"
        self.field_id6 = "RELEASETIME"
        self.field_id7 = "COMMENTS"
        self.field_id8 = "TEL"
        self.field_id9 = "PROTAGONIST"
        self.field_id10 = "@"

        self.dict_file = Dictionary(self.file_name)

        self.dict_file.set_type(self.field_id0, 'D')
        self.dict_file.set_loc(self.field_id0, 0)
        self.dict_file.set_conv(self.field_id0, '')
        self.dict_file.set_name(self.field_id0, 'MOVIES')
        self.dict_file.set_format(self.field_id0, '20L')
        self.dict_file.set_sm(self.field_id0, 'S')
        self.dict_file.set_assoc(self.field_id0, '')
        self.dict_file.set_sql_type(self.field_id0, '')

        self.dict_file.set_type(self.field_id1, 'D')
        self.dict_file.set_loc(self.field_id1, 1)
        self.dict_file.set_conv(self.field_id1, '')
        self.dict_file.set_name(self.field_id1, '国家')
        self.dict_file.set_format(self.field_id1, '20L')
        self.dict_file.set_sm(self.field_id1, 'S')
        self.dict_file.set_assoc(self.field_id1, '')
        self.dict_file.set_sql_type(self.field_id1, '')

        self.dict_file.set_type(self.field_id2, 'D')
        self.dict_file.set_loc(self.field_id2, 2)
        self.dict_file.set_conv(self.field_id2, '')
        self.dict_file.set_name(self.field_id2, '电影名称')
        self.dict_file.set_format(self.field_id2, '20L')
        self.dict_file.set_sm(self.field_id2, 'M')
        self.dict_file.set_assoc(self.field_id2, '')
        self.dict_file.set_sql_type(self.field_id2, '')

        self.dict_file.set_type(self.field_id3, 'D')
        self.dict_file.set_loc(self.field_id3, 3)
        self.dict_file.set_conv(self.field_id3, '')
        self.dict_file.set_name(self.field_id3, '女主角')
        self.dict_file.set_format(self.field_id3, '20L')
        self.dict_file.set_sm(self.field_id3, 'S')
        self.dict_file.set_assoc(self.field_id3, '')
        self.dict_file.set_sql_type(self.field_id3, '')

        self.dict_file.set_type(self.field_id4, 'D')
        self.dict_file.set_loc(self.field_id4, 4)
        self.dict_file.set_conv(self.field_id4, '')
        self.dict_file.set_name(self.field_id4, '男主角')
        self.dict_file.set_format(self.field_id4, '20L')
        self.dict_file.set_sm(self.field_id4, 'S')
        self.dict_file.set_assoc(self.field_id4, '')
        self.dict_file.set_sql_type(self.field_id4, '')

        self.dict_file.set_type(self.field_id5, 'D')
        self.dict_file.set_loc(self.field_id5, 5)
        self.dict_file.set_conv(self.field_id5, '')
        self.dict_file.set_name(self.field_id5, '票房')
        self.dict_file.set_format(self.field_id5, '20L')
        self.dict_file.set_sm(self.field_id5, 'S')
        self.dict_file.set_assoc(self.field_id5, '')
        self.dict_file.set_sql_type(self.field_id5, '')

        self.dict_file.set_type(self.field_id6, 'D')
        self.dict_file.set_loc(self.field_id6, 6)
        self.dict_file.set_conv(self.field_id6, '')
        self.dict_file.set_name(self.field_id6, '上映时间')
        self.dict_file.set_format(self.field_id6, '30L')
        self.dict_file.set_sm(self.field_id6, 'S')
        self.dict_file.set_assoc(self.field_id6, '')
        self.dict_file.set_sql_type(self.field_id6, '')

        self.dict_file.set_type(self.field_id7, 'D')
        self.dict_file.set_loc(self.field_id7, 7)
        self.dict_file.set_conv(self.field_id7, '')
        self.dict_file.set_name(self.field_id7, '影评')
        self.dict_file.set_format(self.field_id7, '30L')
        self.dict_file.set_sm(self.field_id7, 'M')
        self.dict_file.set_assoc(self.field_id7, '')
        self.dict_file.set_sql_type(self.field_id7, '')

        self.dict_file.set_type(self.field_id8, 'D')
        self.dict_file.set_loc(self.field_id8, 8)
        self.dict_file.set_conv(self.field_id8, '')
        self.dict_file.set_name(self.field_id8, '剧务联系方式')
        self.dict_file.set_format(self.field_id8, '20L')
        self.dict_file.set_sm(self.field_id8, 'M')
        self.dict_file.set_assoc(self.field_id8, '')
        self.dict_file.set_sql_type(self.field_id8, '')

        self.dict_file.set_type(self.field_id9, 'I')
        self.dict_file.set_loc(self.field_id9, "ACTRESS:'':ACTOR")
        self.dict_file.set_conv(self.field_id9, '')
        self.dict_file.set_name(self.field_id9, '主演')
        self.dict_file.set_format(self.field_id9, '20L')
        self.dict_file.set_sm(self.field_id9, 'S')
        self.dict_file.set_assoc(self.field_id9, '')
        self.dict_file.set_sql_type(self.field_id9, '')

        self.dict_file.set_type(self.field_id10, 'PH')
        self.dict_file.set_loc(self.field_id10, "COUNTRY MOVIENAME ACTRESS ACTOR BOXOFFICE RELEASETIME COMMENTS PROTAGONIST TEL")
        self.dict_file.set_conv(self.field_id10, '')
        self.dict_file.set_name(self.field_id10, '')
        self.dict_file.set_format(self.field_id10, '')
        self.dict_file.set_sm(self.field_id10, '')
        self.dict_file.set_assoc(self.field_id10, '')
        self.dict_file.set_sql_type(self.field_id10, '')

        self.dict_file.close()

        self.data_file = File(self.file_name)

        self.d1 = DynArray("")
        self.d1.insert(1, "中国")
        self.d1.insert(2, "活着")
        self.d1.insert(3, "巩俐")
        self.d1.insert(4, "葛优")
        self.d1.insert(5, "UNKNOWN")
        self.d1.insert(6, "1994/1/1")
        self.d1.insert(7, "一部讲述苦难的电影")
        self.d1.insert(8, "13512345678")
        self.data_file.write(1, self.d1)

        self.d2 = DynArray("")
        self.d2.insert(1, "美国")
        self.d2.insert(2, "碟中谍")
        self.d2.insert(3, "李美琪")
        self.d2.insert(4, "汤姆克鲁斯")
        self.d2.insert(5, "￥2000000000")
        self.d2.insert(6, "1996/1/1")
        self.d2.insert(7, "讲述特工执行任务的电影")
        self.d2.insert(8, "+1 702 475 6082")
        self.data_file.write(2, self.d2)

        self.d3 = DynArray("")
        self.d3.insert(1, "法国")
        self.d3.insert(2, "放牛班的春天")
        self.d3.insert(3, "玛丽.布奈尔")
        self.d3.insert(4, "杰拉尔")
        self.d3.insert(5, "￥123456.890")
        self.d3.insert(6, "2004年5月6日")
        self.d3.insert(7, "好看\非常好看")
        self.d3.insert(8, "+33 0908070605")
        self.data_file.write(3, self.d3)

        self.d4 = DynArray("")
        self.d4.insert(1, "美国")
        self.d4.insert(2, "泰坦尼克号")
        self.d4.insert(3, "凯特。温丝莱特")
        self.d4.insert(4, "莱昂纳多")
        self.d4.insert(5, "￥14789563.12")
        self.d4.insert(6, "1995年2月14日")
        self.d4.insert(7, "难以被超越的电影")
        self.data_file.write(4, self.d4)

        self.d5 = DynArray("")
        self.d5.insert(1, "中国")
        self.d5.insert(2, ["致青春","狼图腾"])
        self.d5.insert(3, ["杨子珊","昂哈妮玛"])
        self.d5.insert(4, ["赵又廷","冯绍峰"])
        self.d5.insert(5, ["5亿", "未知"])
        self.d5.insert(6, ["2013年4月1日", "2015年4月1日"])        
        self.d5.insert(7, ["赵薇首次执导的电影", "知青养狼的故事"])        
        self.d5.insert(8, ["15923459867", "18901239876"])        
        self.data_file.write(5, self.d5)

        self.data_file.close()

        self.create_test_file30("SAKURO")
        self.file_name = "SAKURO"
        self.field_id0 = "@ID"
        self.field_id1 = "NAME"
        self.field_id2 = "SEX"
        self.field_id3 = "AGE"
        self.field_id4 = "PROFESSION"
        self.field_id5 = "EnglishScore"
        self.field_id6 = "MathScore"
        self.field_id7 = "TotalScore"
        self.field_id8 = "RELATIONSHIP"
        self.field_id9 = "CHARACTER"
        self.field_id10 = "@"        
        
        self.dict_file = Dictionary(self.file_name)

        self.dict_file.set_type(self.field_id0, 'D')
        self.dict_file.set_loc(self.field_id0, 0)
        self.dict_file.set_conv(self.field_id0, '')
        self.dict_file.set_name(self.field_id0, 'SAKURO')
        self.dict_file.set_format(self.field_id0, '20L')
        self.dict_file.set_sm(self.field_id0, 'S')
        self.dict_file.set_assoc(self.field_id0, '')
        self.dict_file.set_sql_type(self.field_id0, '')

        self.dict_file.set_type(self.field_id1, 'D')
        self.dict_file.set_loc(self.field_id1, 1)
        self.dict_file.set_conv(self.field_id1, '')
        self.dict_file.set_name(self.field_id1, '姓名')
        self.dict_file.set_format(self.field_id1, '10L')
        self.dict_file.set_sm(self.field_id1, 'S')
        self.dict_file.set_assoc(self.field_id1, '')

        self.dict_file.set_type(self.field_id2, 'D')
        self.dict_file.set_loc(self.field_id2, 2)
        self.dict_file.set_conv(self.field_id2, '')
        self.dict_file.set_name(self.field_id2, '性别')
        self.dict_file.set_format(self.field_id2, '10L')
        self.dict_file.set_sm(self.field_id2, 'S')
        self.dict_file.set_assoc(self.field_id2, '')

        self.dict_file.set_type(self.field_id3, 'D')
        self.dict_file.set_loc(self.field_id3, 3)
        self.dict_file.set_conv(self.field_id3, '')
        self.dict_file.set_name(self.field_id3, '年龄')
        self.dict_file.set_format(self.field_id3, '10L')
        self.dict_file.set_sm(self.field_id3, 'S')
        self.dict_file.set_assoc(self.field_id3, '')

        self.dict_file.set_type(self.field_id4, 'D')
        self.dict_file.set_loc(self.field_id4, 4)
        self.dict_file.set_conv(self.field_id4, '')
        self.dict_file.set_name(self.field_id4, '职业')
        self.dict_file.set_format(self.field_id4, '15L')
        self.dict_file.set_sm(self.field_id4, 'S')
        self.dict_file.set_assoc(self.field_id4, '')

        self.dict_file.set_type(self.field_id5, 'D')
        self.dict_file.set_loc(self.field_id5, 5)
        self.dict_file.set_conv(self.field_id5, '')
        self.dict_file.set_name(self.field_id5, '英语')
        self.dict_file.set_format(self.field_id5, '15L')
        self.dict_file.set_sm(self.field_id5, 'S')
        self.dict_file.set_assoc(self.field_id5, '')

        self.dict_file.set_type(self.field_id6, 'D')
        self.dict_file.set_loc(self.field_id6, 6)
        self.dict_file.set_conv(self.field_id6, '')
        self.dict_file.set_name(self.field_id6, '数学')
        self.dict_file.set_format(self.field_id6, '15L')
        self.dict_file.set_sm(self.field_id6, 'S')
        self.dict_file.set_assoc(self.field_id6, '')

        self.dict_file.set_type(self.field_id7, 'I')
        self.dict_file.set_loc(self.field_id7, 'SUM(EnglishScore+MathScore)')
        self.dict_file.set_conv(self.field_id7, '')
        self.dict_file.set_name(self.field_id7, '总成绩')
        self.dict_file.set_format(self.field_id7, '15L')
        self.dict_file.set_sm(self.field_id7, 'S')
        self.dict_file.set_assoc(self.field_id7, '')

        self.dict_file.set_type(self.field_id8, 'D')
        self.dict_file.set_loc(self.field_id8, 7)
        self.dict_file.set_conv(self.field_id8, '')
        self.dict_file.set_name(self.field_id8, '与小丸子的关系')
        self.dict_file.set_format(self.field_id8, '20L')
        self.dict_file.set_sm(self.field_id8, 'M')
        self.dict_file.set_assoc(self.field_id8, '')

        self.dict_file.set_type(self.field_id9, 'D')
        self.dict_file.set_loc(self.field_id9, 8)
        self.dict_file.set_conv(self.field_id9, '')
        self.dict_file.set_name(self.field_id9, '人物特点')
        self.dict_file.set_format(self.field_id9, '20L')
        self.dict_file.set_sm(self.field_id9, 'M')
        self.dict_file.set_assoc(self.field_id9, '')

        self.dict_file.set_type(self.field_id10, 'PH')
        self.dict_file.set_loc(self.field_id10, "NAME SEX AGE PROFESSION EnglishScore MathScore TotalScore RELATIONSHIP CHARACTER")
        self.dict_file.set_conv(self.field_id10, '')
        self.dict_file.set_name(self.field_id10, '')
        self.dict_file.set_format(self.field_id10, '')
        self.dict_file.set_sm(self.field_id10, '')
        self.dict_file.set_assoc(self.field_id10, '')

        self.dict_file.close()

        self.data_file = File(self.file_name)

        self.d1 = DynArray("")
        self.d1.insert(1, "樱桃小丸子")
        self.d1.insert(2, "girl")
        self.d1.insert(3, 9)
        self.d1.insert(4, "小学三年级学生")
        self.d1.insert(5, 90)
        self.d1.insert(6, 80)
        self.d1.insert(7, "")
        self.d1.insert(8, ["可爱", "贪玩", "天真", "财迷"])
        self.data_file.write(1, self.d1)

        self.d2 = DynArray("")
        self.d2.insert(1, "小玉")
        self.d2.insert(2, "girl")
        self.d2.insert(3, 9)
        self.d2.insert(4, "学生")
        self.d2.insert(5, 95)
        self.d2.insert(6, 90)
        self.d2.insert(7, ["同桌", "好友"])
        self.d2.insert(8, ["乖巧", "乐于助人","遇到小丸子就犯二"])
        self.data_file.write(2, self.d2)

        self.d3 = DynArray("")
        self.d3.insert(1, "花轮")
        self.d3.insert(2, "boy")
        self.d3.insert(3, 9)
        self.d3.insert(4, "学生")
        self.d3.insert(5, 90)
        self.d3.insert(6, 90)
        self.d3.insert(7, ["同桌"])
        self.d3.insert(8, ["绅士", "喜欢炫耀","阔少爷"])
        self.data_file.write(3, self.d3)

        self.d4 = DynArray("")
        self.d4.insert(1, "丸尾")
        self.d4.insert(2, "boy")
        self.d4.insert(3, 9)
        self.d4.insert(4, "学生")
        self.d4.insert(5, 85)
        self.d4.insert(6, 95)
        self.d4.insert(7, ["同桌"])
        self.d4.insert(8, ["奇怪", "官迷"])
        self.data_file.write(4, self.d4)

        self.d5 = DynArray("")
        self.d5.insert(1, "樱杏子")
        self.d5.insert(2, "girl")
        self.d5.insert(3, 12)
        self.d5.insert(4, "小学六年级学生")
        self.d5.insert(5, 98)
        self.d5.insert(6, 100)
        self.d5.insert(7, ["姐姐"])
        self.d5.insert(8, ["成绩好", "懂事"])
        self.data_file.write(4, self.d5)
        
        self.data_file.close()        
        
    def tearDown(self):
#         self.delete_test_file("MOVIES")
#         self.delete_test_file("MOVIEScp")
#         self.delete_test_file("SAKURO")

        super().tearDown()

    # @classmethod
    # def tearDownClass(cls):
    #     pass

#     def test_cancel(self):
#         cmd = Command()
#         cmd.command_text = "RUN BP TEST_COMMAND"
#         cmd.run()
#         cmd.cancel()
#         self.assertRaises(UOError, cmd.reply, "Hello World!")
#
#     def test_next_response(self):
#         cmd = Command()
#         cmd.command_text = "LIST VOC"
#         cmd.buffer_size = 200
#         cmd.run()
#         while cmd.status == EXEC_MORE_OUTPUT:
#             cmd.next_response()
#         self.assertEqual(cmd.status, uopy.EXEC_COMPLETE)
#
#     def test_buffer_size(self):
#         cmd = Command()
#         cmd.buffer_size = 10
#         cmd.command_text = 'RUN BP TEST_COMMAND'
#         cmd.run()
#         self.assertEqual(cmd.response, 'THIS IS TE')
#
#     def test_reply(self):
#         cmd = Command()
#         cmd.command_text = "RUN BP TEST_COMMAND"
#         cmd.run()
#         cmd.reply("Hello World!")
#         self.assertIn('Hello World!\r\nHello World!\r\n', cmd.response)

    def test_run(self):
        cmd = Command("COUNT VOC")
        cmd.run()
        #self.assertTrue(True)
        self.assertEqual(0, cmd.status)

    def test_AE(self):
        data_file = File("VOC")
        
        dPA = DynArray("")
        dPA.insert(1, "PA")
        dPA.insert(2, "LIST MOVIES 2")
        data_file.write("MOVIES_2", dPA)
                
        cmd=Command()       
        cmd.command_text = "MOVIES_2" 
        cmd.run()
        self.assertIn("1 records listed",cmd.response)  

        cmd1=Command()       
        cmd1.command_text = "DELETE VOC MOVIES_2" 
        cmd1.run()
        self.assertIn("1 records DELETEd",cmd1.response)  
        
    def test_count(self):
        cmd=Command()       
        cmd.command_text = "COUNT MOVIES" 
        cmd.run()
        self.assertIn("records counted",cmd.response)  

    def test_list_voc(self):
        cmd=Command()       
        cmd.command_text = "LIST VOC" 
        cmd.run()
        if cmd.status == uopy.EXEC_REPLY:
            cmd.reply("N")
        self.assertIn("records listed",cmd.response)  

    def test_list_dict(self):
        cmd=Command()       
        cmd.command_text = "LIST DICT MOVIES" 
        cmd.run()
        if cmd.status == uopy.EXEC_REPLY:
            cmd.reply("N")
        self.assertIn("records listed",cmd.response)                          

    def test_list_listf(self):
        cmd=Command()       
        cmd.command_text = "LISTF" 
        cmd.run()
        if cmd.status == uopy.EXEC_REPLY:
            cmd.reply("N")
        self.assertIn("Files listed",cmd.response)           

    def test_list_sample(self):   
        cmd=Command()       
        cmd.command_text = "LIST MOVIES SAMPLE 2" 
        cmd.run()
        self.assertIn("Sample of 2 records listed",cmd.response) 

    def test_list_nosplit(self): 
        cmd=Command()       
        cmd.command_text = "LIST MOVIES=2 NO-SPLIT" 
        cmd.run()
        self.assertIn("1 records listed",cmd.response) 

    def test_list_like(self):
        cmd=Command()       
        cmd.command_text = "LIST MOVIES WITH COUNTRY LIKE '法国'" 
        cmd.run()
        self.assertIn("1 records listed",cmd.response) 
                        
        cmd1=Command()       
        cmd1.command_text = "LIST MOVIES WITH COUNTRY='中国'" 
        cmd1.run()
        self.assertIn("records listed",cmd1.response) 

    def test_list_toxml(self):
        cmd=Command()       
        cmd.command_text = "LIST MOVIES TOXML" 
        cmd.run()
        self.assertIn("</ROOT>",cmd.response)         

    def test_list_sort(self):              
        cmd=Command()       
        cmd.command_text = "SORT MOVIES WITH COUNTRY='中国'" 
        cmd.run()
        if cmd.status == uopy.EXEC_REPLY:
            cmd.reply("N")
        self.assertIn("records listed",cmd.response) 

    def test_copy(self):
        cmd=Command()       
        cmd.command_text = "COPY FROM DICT MOVIES TO MOVIEScp ALL OVERWRITING" 
        cmd.run()
        self.assertIn("records copied",cmd.response) 

    def test_como(self):
        cmd=Command()       
        cmd.command_text = "COMO ON test" 
        cmd.run()
        self.assertIn("established",cmd.response)

        cmd1=Command()       
        cmd1.command_text = "LIST MOVIES WITH COUNTRY='中国'" 
        cmd1.run()

        cmd2=Command()       
        cmd2.command_text = "COMO OFF" 
        cmd2.run()
        self.assertIn("COMO completed",cmd2.response)

        cmd2=Command()       
        cmd2.command_text = "CT &COMO& test" 
        cmd2.run()
        self.assertIn("中国",cmd2.response)
        
        cmd3=Command()       
        cmd3.command_text = "DELETE &COMO& test" 
        cmd3.run() 

    def test_select(self):
        cmd1=Command()       
        cmd1.command_text = "SELECT MOVIES WITH COUNTRY='美国'" 
        cmd1.run()        
        self.assertIn("2 record(s) selected",cmd1.response)

        cmd2=Command()       
        cmd2.command_text = "COUNT MOVIES" 
        cmd2.run()        
        self.assertIn("2 records counted",cmd2.response)

    def test_acreateBPfolder(self):
        cmd1=Command()       
        cmd1.command_text = "CREATE.FILE UOPYBP 19" 
        cmd1.run()        
        self.assertIn("to \"D_UOPYBP\"",cmd1.response)
        
        cmd2=Command()       
        cmd2.command_text = "DELETE.FILE UOPYBP" 
        cmd2.run()        

    def test_za_basicprogram(self): 
        data_file = File("BP")
        d1 = DynArray("")
        d1.insert(1, "DATA \"中国China\"")
        d1.insert(2, "INPUT BBB")
        data_file.write("health", d1) 
               
        cmd1=Command()       
        cmd1.command_text = "BASIC BP health" 
        cmd1.run()        
        self.assertIn("Compilation Complete",cmd1.response)

        cmd2=Command()       
        cmd2.command_text = "CATALOG BP health FORCE" 
        cmd2.run()        
        self.assertIn("cataloged",cmd2.response)

        cmd3=Command()       
        cmd3.command_text = "health" 
        cmd3.run()        
        self.assertIn("China",cmd3.response)

        cmd5=Command()       
        cmd5.command_text = "DECATALOG BP health" 
        cmd5.run()  
        
        cmd4=Command()       
        cmd4.command_text = "DELETE BP health" 
        cmd4.run()        

    def test_zb_pythonprogram(self):
        with SequentialFile("PP", "inputprogram.py",True) as py_file:
            py_file.write_line("s=\"凯特\"")
            py_file.write_line("print(\"你好\",s)")
          
        cmd=Command()       
        cmd.command_text = "RUNPY PP inputprogram.py" 
        cmd.run()  

        self.assertIn("凯特",cmd.response)
        
        cmd1=Command()       
        cmd1.command_text = "DELETE PP inputprogram.py" 
        cmd1.run()
        
    def test_zc_subrutine(self):
        with SequentialFile("BP", "subtest",True) as sr_file:
            sr_file.write_line("SUBROUTINE subtest(p1,p2)")
            sr_file.write_line("PRINT p1,p2")        

        cmd1=Command()       
        cmd1.command_text = "BASIC BP subtest" 
        cmd1.run()        

        cmd2=Command()       
        cmd2.command_text = "CATALOG BP subtest FORCE" 
        cmd2.run()        

        sub = Subroutine("subtest", 2)
        sub.args[0] = "你好"
        sub.args[1] = "大连0411"
        sub.call()
        self.assertIn("大连", str(sub.args))

        cmd5=Command()       
        cmd5.command_text = "DECATALOG BP subtest" 
        cmd5.run()
                 
        cmd3=Command()       
        cmd3.command_text = "DELETE BP subtest" 
        cmd3.run()  
        
    def test_cmdInError(self):
        cmd1=Command()       
        cmd1.command_text = "WHO" 
        self.assertRaises(TypeError, Command.run,cmd1,"am i")
        self.assertRaises(TypeError, Command.run,"LIST MOVIES","LIST DICT MOVIES")                
        
if __name__ == '__main__':
    unittest.main()
