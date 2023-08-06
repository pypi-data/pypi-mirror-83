#coding=utf-8
from uopy import UOError, EXEC_MORE_OUTPUT, SequentialFile, Command, Dictionary, File, DynArray, Subroutine
from tests.unitestbase_cn import *
import os

class TestDynArrayCn(UniTestBaseCn):
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
        self.dict_file.set_format(self.field_id0, '10L')
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
        self.dict_file.set_format(self.field_id2, '10L')
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
        self.data_file.write(5, self.d5)
        
        self.data_file.close()        
        
    def tearDown(self):
        self.delete_test_file("MOVIES")
        self.delete_test_file("MOVIEScp")
        self.delete_test_file("SAKURO")

        super().tearDown()

    def test_exerciseOnly(self):
        d=DynArray()
        d.insert(0,["a", "c"])
        d.insert(1,"b")
        d.insert(2,[["d", "e"]])
        self.assertEqual(d,b'a\xfdc\xfeb\xfed\xfce' )
        
        d = DynArray([""])
        d.make_list(0)
        d[0].append("1")
        d.insert(1,"2")
        d.insert(2,["3", "4"])
        d.make_nested_list(2)
        d[2][1].append("5")
#         print(bytes(d))
#         print(d.list)        
        self.assertEqual(d, [['', '1'],'2',[['3'], ['4','5']] ] )
        self.assertEqual(d,b'\xfd1\xfe2\xfe3\xfd4\xfc5' )

        d = DynArray([1, 2, [[3], 4] ])
#         print(bytes(d))
        d.make_nested_list(2)
        d[2][1].append(98)
#         print(bytes(d))
        self.assertEqual(d, [1, 2, [[3], [4, 98]] ])
        self.assertEqual(d,b'1\xfe2\xfe3\xfd4\xfc98')
        
        d=DynArray()
        d.insert(0,["a", ["t",""] ] )
#         d.make_nested_list(0)
        print(bytes(d))
        self.assertEqual(d,b'a\xfdt\xfc')
        print(d[0][1][0])
        
        d = DynArray()
        d.append(["",["", "", "sm"]])
        print(d.list)
        print(bytes(d))  
        
        d = DynArray([["汤姆克鲁斯", "米歇尔.莫娜汉"]])
        print(len(d))      

        d = DynArray()
        d1 = DynArray()
        d.insert(0,"美国电影")
        d.insert(1,"碟中谍")
        d.insert(2,"特工系列")
        d.insert(3,["汤姆克鲁斯", "米歇尔。莫娜汉"])
        d.insert(4,[["汤姆克鲁斯-苏瑞", "unknow"]])
        d.insert(5,"票房￥1000000000")
        print(d)
        for i in d:
            print(i,"",type(i))   
        
        print("#########################################################################")
        d = DynArray()
        d.insert(0,["汤姆克鲁斯", "米歇尔。莫娜汉"])
        d.insert(1,"碟中谍")
        d.insert(2,[["汤姆克鲁斯-苏瑞", "unknow"]])
#         print(d)
        for i in d:
            if type(i) == list:
                for v in i:
                    if type(v) == list:
                        for sv in v:
                            print(sv,": ",type(sv))
                    else:
                        print(v,": ",type(v))
            else:
                print(i,": ",type(i))

        d = DynArray()
        d.append("ss")
        self.assertEqual(str(d), str('ss'))
        d.insert(1,[["", "dd"]])
        print(bytes(d))
                                 
    def test_dynarrayarg(self):
        d = DynArray()
        d.insert(0,"美国电影")
        d.insert(1,"碟中谍")
        d.insert(2,"特工系列")
        d.insert(3,["汤姆克鲁斯", "米歇尔.莫娜汉"])
        d.insert(4,[["苏瑞"]])
        self.assertEqual(str(d[0]),"美国电影" )
        self.assertEqual(str(d[4][0][0]),"苏瑞" )

    #Directory dynamic array
    def test_bdirectoryarray(self):
        f = File("SAKURO")
        r = f.read(1)
        self.assertEqual(str(r[0]),'樱桃小丸子')
        self.assertEqual(str(r[1]),'girl')
        f.close()
                  
        f = Dictionary("SAKURO") 
        r = f.read("NAME")       
        self.assertEqual(str(r[0]),'D')    
        self.assertEqual(str(r[3]),'姓名')   
        f.close()

    # The count method  D.count(substring) -> integer -- return the number of times a substring is repeated in the dynamic array       
    def test_count(self):
        # Positive cases
        d = DynArray("中国")
        d.append("中")
        self.assertEqual(d.count("中"), 1) 

        d = DynArray("￥")
        self.assertEqual(d.count("￥"),1)

        d = DynArray("中国美国英国法国")
        d.append("国")
        d.append("国")
        d.append("国")
        d.append("国")
        self.assertEqual(d.count("国"),4) 
        self.assertEqual(d.count("玉"),0) 

        d = DynArray("中国 ￥中国 ￥中国")
        d.append("￥")
        d.append("￥")        
        self.assertEqual(d.count("￥"),2)
        
        d = DynArray("中国 China中国")
        d.append(" ")
        self.assertEqual(d.count(" "),1) 
        
        d = DynArray("……")
        self.assertEqual(d.count("."),0)  

        d = DynArray()
        d.insert(0,"美国电影")
        d.insert(1,"碟中谍")
        d.insert(2,"特工系列")
        d.insert(3, ["汤姆克鲁斯", "米歇尔。莫娜汉"])
        d.insert(4,[["unknown", "汤姆克鲁斯-苏瑞"]])
        d.insert(5,"票房￥1000000000") 
 
        self.assertEqual(d.count(["汤姆克鲁斯", "米歇尔。莫娜汉"]),1)

        f = File("MOVIES")
        r = f.read(1)
        self.assertEqual(r.count("巩俐"),1)
        r = f.read(5)
        self.assertEqual(r.count(["致青春","狼图腾"]),1)
        self.assertEqual(r.count(["杨子珊","昂哈妮玛"]),1)
        self.assertEqual(r.count(["赵薇首次执导的电影", "知青养狼的故事"]),1)
        f.close()

        f = Dictionary("MOVIES")
        r = f.read("ACTRESS")
        self.assertEqual(r.count("女主角"), 1)
        self.assertEqual(r.count("M"), 0)
        self.assertEqual(r.count("S"), 1)
        f.close()

        f = Dictionary("MOVIES")
        r = f.read("PROTAGONIST")

        self.assertEqual(r.count("主演"), 1)
        self.assertEqual(r.count("ACTRESS:'':ACTOR"), 1) 
        f.close() 

        #directory dynamic file              
        f = File("SAKURO")
        r = f.read(3)
#         print(str(r))          
        self.assertEqual(r.count("花轮"), 1)
        self.assertEqual(r.count(["绅士", "喜欢炫耀","阔少爷"]), 1)
        f.close()

        #directory dynamic dict file
        f = Dictionary("SAKURO")
        r = f.read("SEX")
        self.assertEqual(r.count("性别"),1)
        self.assertEqual(r.count("D"),1)
        self.assertEqual(r.count("A"),0) 
        self.assertEqual(r.count("Max"),0) 
        f.close() 

        # Negative cases       
        d = DynArray("测试用")
        #Error:function takes exactly 1 argument (2 given)
        self.assertRaises(TypeError, d.count,"x",1)
        #Error:function takes exactly 1 argument (0 given)
        self.assertRaises(TypeError, d.count)
        #Error:function takes exactly 1 argument (6 given)
        self.assertRaises(TypeError, d.count,"@","#","￥","%","……","&")
 
    # The delete method  D.delete(field#, [value#, [subvalue#]]) -> None -- delete a field, value or subvalue from the dynamic array        
    def test_delete(self):      
        # Positive cases 
        d = DynArray()
        self.assertEqual(bytes(d),b'')

        d = DynArray()
        d.insert(0,"美国电影")
        d.insert(1,"碟中谍")
        d.insert(2,"特工系列")
        d.insert(3, ["汤姆克鲁斯", "米歇尔。莫娜汉"])
        d.insert(4,[["unknown", "汤姆克鲁斯-苏瑞"]])
        d.insert(5,"票房￥1000000000") 
        self.assertEqual(str(d[0]),'美国电影')
        d.remove("美国电影")
        self.assertEqual(str(d[0]),'碟中谍')
        self.assertEqual(str(d[2][0]),"汤姆克鲁斯")
        d[2].pop(0)
        self.assertEqual(str(d[2][0]),'米歇尔。莫娜汉')
        
        f = File("MOVIES")
        d = f.read(1)
        a = d[2]
        d.pop(2)
        self.assertNotIn(str(a),str(d))        
        d = f.read(5)
        a = d[2]
        d.pop(2)
        self.assertNotIn(str(a),str(d))
        f.close()
                
        f = Dictionary("MOVIES")
        d = f.read("COMMENTS")
#         print(str(d))
        a = d[4]
        d.pop(4)
        self.assertNotIn(str(a), str(d))
        f.close() 

        #directory dynamic file              
        f = File("SAKURO")
        d = f.read(1)
        a = d[1]
        d.pop(1)
        self.assertNotIn(str(a), str(d))
        f.close()

        #directory dynamic dict file
        f = Dictionary("SAKURO")
        d = f.read("AGE")
#         print(str(d))
        a = d[4]
        d.pop(4)
        self.assertNotIn(bytes(str(a),'utf-8'), bytes(str(d),'utf-8'))
        f.close() 

     #Negative cases
        d = DynArray("测试用")
        #Error: an integer is required (got type str)                 
        self.assertRaises(TypeError, d.pop,"123")
        #Error: function takes at most 3 arguments (4 given)
        self.assertRaises(TypeError, d.pop,1,2,3,4)                        

        #Use the special character
        #Error: an integer is required (got type str)  
        self.assertRaises(TypeError, d.pop,"*")
        self.assertRaises(TypeError, d.pop,"*","……")

    # The extract method D.extract(field#, [value#, [subvalue#]]) -> new DynArray object -- extract a field, 
    # a value, or a subvalue from the dynamic array
    def test_extract(self):
        # Positive cases 
        f = File("MOVIES")
        d = f.read(5)
        a = d[1]
        self.assertEqual(str(a[0]),str("致青春"))
        self.assertEqual(str(a[1]),str("狼图腾"))
        f.close()

        f = Dictionary("MOVIES")
        d = f.read("COMMENTS")
        a = d[3]
        self.assertEqual(str(a), str("影评"))
        f.close()    

        #directory dynamic file             
        f = File("SAKURO")
        d = f.read(3)
        a = d[2]
#         print(d)
        self.assertEqual(bytes(a,'utf-8'), b'9')
        a = d[7][1]
        self.assertEqual(str(a), str('喜欢炫耀'))
        f.close()

        #directory dynamic dict file
        f = Dictionary("SAKURO")
        d = f.read("RELATIONSHIP")
        a = d[3]
        self.assertEqual(str(a),str('与小丸子的关系')) 
        f.close()

    # The format method  D.format(codes) -> new DynArray object -- format data in the dynamic array with formatting codes         
    def test_format(self):
        #Postive cases
        d = DynArray("这是一个测试用例")
        f = d.format('2L')
        self.assertEqual(str(f), str('这是'))
        f = d.format('2L')
        self.assertEqual(str(f), str('这是'))

        d = DynArray("中")
        f = d.format("10C")
        self.assertEqual(str(f[0]), str('    中     '))

        d = DynArray()
        d.insert(1,"中国人民银行")
        f = d.format("8L##-##-##")
        self.assertEqual(str(f[0]), str('中国-人民-银行'))

        d = DynArray()
        d.insert(1,"中国人民银行")
        f = d.format("20R")
        self.assertEqual(str(f), str('              中国人民银行'))
        f1 = d.format("20L")
        self.assertEqual(str(f1), str('中国人民银行              '))

        f = File("MOVIES")
        d = f.read(3)
        s = d[0].format("50@R")
        self.assertEqual(str(s),'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@法国')
        s = d[1].format("10C")
        self.assertEqual(str(s),'  放牛班的春天  ')
        s = d[1].format("11#-#-#-#-#-#")
        self.assertEqual(str(s),'放-牛-班-的-春-天')
        f.close()

        f = Dictionary("MOVIES")
        d = f.read("ACTOR")
        s = d[3].format("5L")       
        self.assertEqual(str(s),str('男主角  '))
        f.close()

        #directory dynamic file          
        f = File("SAKURO")
        d = f.read(1)
        s = d[0].format("10L")
        self.assertEqual(str(s), str('樱桃小丸子     '))
        f.close()

        #directory dynamic dict file
        f = Dictionary("SAKURO")
        d = f.read("RELATIONSHIP")
        s = d[3].format("10L#-###-#-##")
        self.assertEqual(str(s),str('与-小丸子-的-关系'))
        f.close()

        # Negative cases
        d = DynArray("测试用")
        #Error:function takes exactly 1 argument (0 given)
        self.assertRaises(TypeError, d.format)
        #Error:function takes exactly 1 argument (2 given)      
        self.assertRaises(TypeError, d.format,"60R","B")
        self.assertRaises(TypeError, d.format,"￥","……")

    # The iconv method  D.iconv(convcode) -> new DynArray object -- convert the dynamic array to a specified internal storage format  
    def test_iconv(self):
        # Positive cases
        d = DynArray("中国红")
        i = d.iconv("T1,2")
        self.assertEqual(str(i),str("中国" ))
        i = d.iconv("L")
        self.assertEqual(bytes(i), b'3')

        d = DynArray()  
        d.insert(1,'中国红ChineseRed')
        i = d.iconv("L")
        self.assertEqual(bytes(i), b'13')

        d = DynArray()
        d.insert(1,"汉字abc")
        i = d.iconv("MCU")
        self.assertEqual(str(i), str('汉字ABC'))

        # a time format in a dynamic array won't change by format method.
        f = File("MOVIES")
        d = f.read(2)
        d.insert(9,"10:20")
        d1=DynArray(d[8])
        i = d1.iconv("MT")
        self.assertEqual(bytes(i), b'37200')

        d = f.read(1)
        d1=DynArray(d[7])
        i = d1.iconv("R13512345671,13512345679")
        #i=13512345678
        self.assertEqual(bytes(i), b'13512345678')
        i1 = d1.iconv("R1,2")
        self.assertEqual(bytes(i1), b'')
        f.close()

        f = Dictionary("MOVIES")
        d = f.read("BOXOFFICE")
        i = d.insert(9,"12.335")
        d1=DynArray(d[8])    
        ic = d1.iconv("MR2")
        self.assertEqual(str(ic),str('1234'))        
        f.close()

        d = DynArray("中国+艾米")
        i = d.iconv("G1+1")
        self.assertEqual(str(i), str('艾米'))          

        #directory dynamic file             
        f = File("SAKURO")
        d = f.read(1)
        # d.extract(2) girl
        d1=DynArray(d[1])
        i = d1.iconv("MCU") 
        self.assertEqual(bytes(i), b'GIRL')
        # d.extract(5) 90
        d2=DynArray(d[4])        
        i = d2.iconv("ML2")
        self.assertEqual(bytes(i), b'9000')
        f.close()

        #directory dynamic dict file
        f = Dictionary("SAKURO")
        d = f.read("NAME")
        #d.extract(1) 'D'
        d1=DynArray(d[0])
        i = d1.iconv("MX") 
        self.assertEqual(bytes(i),b'13')
        f.close()

        # Negative cases
        d = DynArray("测试用")
        #Error: function takes exactly 1 argument (0 given)
        self.assertRaises(TypeError, d.iconv) 
        #Error:function takes exactly 1 argument (2 given)     
        self.assertRaises(TypeError, d.iconv,"MT","MCU")
        #Error:TypeError: must be str, not int
        self.assertRaises(UOError, d.iconv,1)  

#    # The insert method  D.insert(field#, [value#, [subvalue#]], insert.value) -> None -- insert a new field, value, or subvalue into the dynamic array
    def test_insert(self):
        # positive cases  
        f = File("MOVIES")
        d = f.read(4)
        d.append("奥斯卡大奖影片")
        self.assertEqual(str(d[7]),str("奥斯卡大奖影片"))
        
        d.insert(9,["￥123456789.0123",["北国风光，千里冰封，万里雪飘。望长城内外，惟余莽莽；大河上下，顿失滔滔。山舞银蛇，原驰蜡象，欲与天公试比高。须晴日，看红装素裹，分外妖娆。 江山如此多娇，引无数英雄竞折腰。 惜秦皇汉武，略输文采；唐宗宋祖，稍逊风骚。一代天骄，成吉思汗，只识弯弓射大雕。俱往矣，数风流人物，还看今朝。",""]])
        self.assertEqual(str(d[8][0]),str("￥123456789.0123"))
        self.assertEqual(str(d[8][1][0]),str('北国风光，千里冰封，万里雪飘。望长城内外，惟余莽莽；大河上下，顿失滔滔。山舞银蛇，原驰蜡象，欲与天公试比高。须晴日，看红装素裹，分外妖娆。 江山如此多娇，引无数英雄竞折腰。 惜秦皇汉武，略输文采；唐宗宋祖，稍逊风骚。一代天骄，成吉思汗，只识弯弓射大雕。俱往矣，数风流人物，还看今朝。'))
            
        d = f.read(5)
        d1=d[1]
        d1.insert(0,"赤壁")
        self.assertEqual(str(d1[0]),str("赤壁"))
        self.assertEqual(str(d1[1]),str("致青春"))
        self.assertEqual(str(d1[2]),str("狼图腾"))        
        f.close()

        # CreateFile3file3 a dynamic array by dict file record
        f = Dictionary("MOVIES")
        d = f.read("@ID")
        d.insert(0,["","数据类型"])
        d1=d[0]
        self.assertEqual(str(d1[1]),str("数据类型"))
        d.insert(100,["Data Type",""])
        d2=d[9]       
        self.assertEqual(str(d2[0]),str("Data Type"))       
        f.close()

        d = DynArray()
#         d.insert(1,2,3,"夏天")
        d.append(["",["", "", "夏天"]])
        d1=d[0][1]
        self.assertEqual(str(d1[2]), str('夏天'))
        d.insert(1,"！@#￥%……&*（）")
        self.assertEqual(str(d[1]), str('！@#￥%……&*（）'))
        d.insert(2,"tour")
        self.assertEqual(str(d[2]), str('tour'))

       #directory dynamic file        
        f = File("SAKURO")
        d = f.read(5)
        d.insert(6,["","","手工课好"])
        d1=d[6] 
        self.assertEqual(str(d1[2]), str('手工课好'))
        f.close()

        #directory dynamic dict file
        f = Dictionary("SAKURO")
        d = f.read('AGE')
        d.insert(10,'都是小孩子')
        self.assertEqual(str(d[7]),str('都是小孩子'))
        f.close()

        # Negative cases
        d = DynArray("测试用")
        # Error insert() takes 2 - 4 arguments (1 given) 
        self.assertRaises(TypeError, d.insert,1) 
        #Error insert() takes 2 - 4 arguments (5 given)     
        self.assertRaises(TypeError, d.insert,1,2,3,1,"Lucy")
        #Error: an integer is required (got type str)
        self.assertRaises(TypeError, d.insert,1,"A","Lucy")
        #Error: an integer is required (got type str)
        self.assertRaises(TypeError, d.insert,1,2,"A","Lucy") 

    #D.locate(field#, [value#, [subvalue#]], search.value, [search.order]. search.value) -> new Python dict object -- search for a field, value, or subvalue in the dynamic array
    #returns a Python dict object with two keys: 'found' and 'index'. the value of 'found' is either True or False, the value of 'index' indicates where search.value was 
    #found in the dynamic array or where search.value should be inserted in the dynamic array if it was not found
    def test_locate(self):
        # positive cases
        d = DynArray("中")
        l = d.index("中")
        self.assertEqual(l, 0)
 
        d = DynArray()
        d.insert(1,"壹")
        d.insert(2,"贰")
        d.insert(7,"柒")
        l = d.index("柒")
        self.assertEqual(l, 2) 

        f = File("MOVIES")
        d = f.read("3")
        l = d.index("法国")
        self.assertEqual(l, 0)
        d = f.read(5)
        l = d.index(['杨子珊', '昂哈妮玛'])
        self.assertEqual(l, 2)                
        f.close()  

        # CreateFile3file3 a dynamic array by dict file record
        f = Dictionary("MOVIES")
        d = f.read("BOXOFFICE")
        l = d.index("D")
        self.assertEqual(l, 0)
        f.close()

        #directory dynamic file           
        f = File("SAKURO")
        d = DynArray(f.read(5))
        l = d.index("樱杏子")
        self.assertEqual(l, 0)
        f.close()

        #directory dynamic dict file
        f = Dictionary("SAKURO")
        d = f.read("CHARACTER")
        l = d.index("20L")
        self.assertEqual(l, 4)
        d.insert(10,"rainbow")
        l = d.index("rainbow")
        self.assertEqual(l, 7)
        f.close()
        
        #Negative cases
        d = DynArray("测试用")
        #TypeError: locate() takes 2 - 5 arguments (1 given)
        self.assertRaises(ValueError,d.index,1)
        #TypeError: locate() takes 2 - 5 arguments (6 given)
        self.assertRaises(TypeError,d.index,1,2,3,4,5,"") 
        #Error: an integer is required (got type str)
        self.assertRaises(TypeError,d.index,"……",'中国')

    # The oconv method   D.oconv(convcode) -> new DynArray object -- convert the dynamic array to a specified format for output 
    def test_oconv(self):
        # Positive cases
        d = DynArray("中国")
        o1 = d.oconv("L")
        self.assertEqual(bytes(o1), b'2')
        o2 = d.oconv("L1,3")
        self.assertEqual(str(o2), str('中国'))
        o2 = d.oconv("L3,5")
        self.assertEqual(str(o2), str(''))

        d = DynArray("rose玫瑰1314")
        o1 = d.oconv("MCU")
        self.assertEqual(str(o1), str('ROSE玫瑰1314'))
        o2 = d.oconv("MCA")
        self.assertEqual(str(o2), str('rose'))
        o3 = d.oconv("MC/A")
        self.assertEqual(str(o3), str('玫瑰1314'))
        o4 = d.oconv("MCN")
        self.assertEqual(bytes(o4),b"1314")
        o5 = d.oconv("MC/N")
        self.assertEqual(str(o5),str("rose玫瑰"))

        f = Dictionary("MOVIES")
        d = f.read("MOVIENAME")
        #d=b'D\xfe10\xfe\xfeLead Actors\xfe35L\xfeMV' OCONV(str.expr, "T[m,]n")
        o = d.oconv("T1,5")
        self.assertEqual(bytes(o), b'D\xfe2\xfe\xfe')
        f.close()

        #directory dynamic file            
        f = File("SAKURO")
        d = f.read(1)
        #MCA Extracts all alphabetic characters
        o = d.oconv("MCA")
        self.assertEqual(bytes(o), b'girl')
        f.close()

        #directory dynamic dict file
        f = Dictionary("SAKURO")
        d = f.read("NAME")
        d3=DynArray(d[3])
        #MC/A Extracts all nonalphabetic characters.
        o = d3.oconv("MC/A")
        self.assertEqual(str(o), '姓名') 
        f.close()

        # Negative cases
        d = DynArray("测试用")
        #Error function takes exactly 1 argument (0 given)
        self.assertRaises(TypeError, d.oconv)
        #Error:must be str, not int
        self.assertRaises(UOError, d.oconv,1)
        #Error:function takes exactly 1 argument (2 given)
        self.assertRaises(TypeError, d.oconv,"MX","R")
        self.assertRaises(TypeError, d.oconv,"￥","……")

    def test_replace(self):
        #Positive cases
        #a empty dynamic array
        d = DynArray()
        d.insert(0,"中国")
        self.assertEqual(str(d), str('中国'))
        d.insert(1,["", ["", "大连"]])
        d1=d[1][1]
        self.assertEqual(str(d1[1]),str('大连'))

        d = DynArray()
        d.append("￥￥￥")
        self.assertEqual(str(d), str('￥￥￥'))
        d.append("大连DaLian")
        self.assertEqual(str(d[1]), str('大连DaLian'))

        f = File("MOVIES")
        d = f.read(2)
        d[1]="Denver"
        self.assertEqual(str(d[1]),str('Denver'))
        d[6]=["","", ["", "余华著"]]
#         d.replace(8,3,2,"余华著" )
        d6=d[6][2]
        self.assertEqual(str(d6[1]),str('余华著'))
        f.close()

        f = Dictionary("MOVIES")
        d = f.read("RELEASETIME")
#         d.replace(2,"丹佛" )
        d[1]="丹佛"
        self.assertEqual(str(d[1]),str('丹佛'))
#         d.replace(2,2,2,"什么时候上映?")
        d[1]=["", ["","什么时候上映?"]]
        d1=d[1][1]
        self.assertEqual(str(d1[1]),str('什么时候上映?'))
#         d.replace(2,2,2,"首映时间" )
        d[1]=["", ["","首映时间"]]
        d1=d[1][1]
        self.assertEqual(str(d1[1]),str('首映时间'))
        f.close()

        #directory dynamic file          
        f = File("SAKURO")
        d = f.read(1)
        d[0]="可爱的小丸子"
        self.assertEqual(str(d[0]),str('可爱的小丸子'))        
#         d.replace(6,5,"真实")
        d[5]=["", "", "", "", "真实"]
        d5=d[5][4]
        self.assertEqual(str(d5),str('真实'))
        f.close()

        #directory dynamic dict file
        f = Dictionary("SAKURO")
        d = f.read("NAME")
#         d.replace(-2,'测试')
        d[-2]= '测试'     
        self.assertEqual(str(d[-2]),str('测试')) 
        f.close()

        # Negative cases
        d = DynArray("测试用")
        self.assertRaises(TypeError, d[0])
        self.assertRaises(TypeError, d[0],"")
        self.assertRaises(TypeError, d[0]," ")
        self.assertRaises(TypeError, d[0],1)
        self.assertRaises(TypeError, d[0],1,2,3,"BYE","Bye")
        self.assertRaises(TypeError, d[0],1,2,3,4,"BYE")
        #Error: an integer is required (got type str)
        self.assertRaises(TypeError, d[0],"……","￥","*","中国")
                                                      
    def test_eq(self):
        a = DynArray("中国")
        b = DynArray("中国")
        c = DynArray("美国")
        self.assertEqual(a,b)
        self.assertNotEqual(a,c)

        a = DynArray()
        a.insert(0,"中国")
        a.insert(1,["大", "连"])
        b = DynArray()
        b.insert(0,"中国")
        b.insert(1,"大")
        b.insert(2,"连")
        self.assertNotEqual(a,b)

        f = File("MOVIES")
        d1 = f.read("3")
        d2 = f.read("1")
        self.assertNotEqual(d1,d2)
        f.close()

        #dict file
        f = Dictionary("MOVIES")
        d1 = f.read("ACTOR")
        d2 = f.read("COUNTRY")
        self.assertNotEqual(d1,d2)
        f.close()

        # dir file
        f = File("SAKURO")
        d1 = f.read(1)
        d2 = f.read(2)
        self.assertNotEqual(d1,d2)        
        f.close()

        #dir dict file
        f = Dictionary("SAKURO")
        d1 = f.read("AGE")
        d2 = f.read("NAME")
        self.assertNotEqual(d1,d2)        
        f.close()

    def test_iterdynarray(self):
        d = DynArray()
        d1 = DynArray()
        d.insert(0,"美国电影")
        d.insert(1,"碟中谍")
        d.insert(2,"特工系列")
        d.insert(3,["汤姆克鲁斯", "米歇尔。莫娜汉"])
        d.insert(4,[["汤姆克鲁斯-苏瑞", "unknow"]])
        d.insert(5,"票房￥1000000000")
        n = 0
        
        for i in d:
            if type(i) == list:
                for v in i:
                    if type(v) == list:
                        for sv in v:
                            d1.insert(n,[sv,n])
                            n=n+1                            
                    else:
                        d1.insert(n,[v,n])
                        n=n+1                        
            else:
                d1.insert(n,[i,n])
                n=n+1

        self.assertEqual(d1[0],['美国电影', 0])
        self.assertEqual(d1[1],['碟中谍', 1])
        self.assertEqual(d1[2],['特工系列', 2])
        self.assertEqual(d1[3],['汤姆克鲁斯', 3])
        self.assertEqual(d1[4],['米歇尔。莫娜汉', 4])
        self.assertEqual(d1[5],['汤姆克鲁斯-苏瑞', 5])
        self.assertEqual(d1[6],['unknow', 6])
        self.assertEqual(d1[7],['票房￥1000000000', 7])

    def test_iterfile(self): 
        f = File("MOVIES")
        d = f.read(1)
        d1 = DynArray()
        n = 0
        
        for i in d:
            if type(i) == list:
                for v in i:
                    if type(v) == list:
                        for sv in v:
                            d1.insert(n,[sv,n])
                            n=n+1                            
                    else:
                        d1.insert(n,[v,n])
                        n=n+1                        
            else:
                d1.insert(n,[i,n])
                n=n+1
        f.close()
        
        self.assertEqual(d1[0],['中国', 0])
        self.assertEqual(d1[1],['活着', 1])
        self.assertEqual(d1[2],['巩俐', 2])
        self.assertEqual(d1[3],['葛优', 3])
        self.assertEqual(d1[4],['UNKNOWN', 4])
        self.assertEqual(d1[5],['1994/1/1', 5])
        self.assertEqual(d1[6],['一部讲述苦难的电影', 6])
        self.assertEqual(d1[7],['13512345678', 7])

    def test_dictfile(self): 
        f = Dictionary("MOVIES")
        d = f.read("COMMENTS")
        d1 = DynArray()
        n = 0
        
        for i in d:
            if type(i) == list:
                for v in i:
                    if type(v) == list:
                        for sv in v:
                            d1.insert(n,[sv,n])
                            n=n+1                            
                    else:
                        d1.insert(n,[v,n])
                        n=n+1                        
            else:
                d1.insert(n,[i,n])
                n=n+1
        f.close()
        
        self.assertEqual(d1[0],['D', 0])
        self.assertEqual(d1[1],['7', 1])
        self.assertEqual(d1[2],['', 2])
        self.assertEqual(d1[3],['影评', 3])
        self.assertEqual(d1[4],['30L', 4])
        self.assertEqual(d1[5],['M', 5])
        self.assertEqual(d1[6],['', 6])
        self.assertEqual(d1[7],['', 7])

    def test_dirfile(self):
        f = File("SAKURO")
        d = f.read(3)
        d1 = DynArray()
        n = 0
        
        for i in d:
            if type(i) == list:
                for v in i:
                    if type(v) == list:
                        for sv in v:
                            d1.insert(n,[sv,n])
                            n=n+1                            
                    else:
                        d1.insert(n,[v,n])
                        n=n+1                        
            else:
                d1.insert(n,[i,n])
                n=n+1
        f.close()
        
        self.assertEqual(d1[0],['花轮', 0])
        self.assertEqual(d1[1],['boy', 1])
        self.assertEqual(d1[2],['9', 2])
        self.assertEqual(d1[3],['学生', 3])
        self.assertEqual(d1[4],['90', 4])
        self.assertEqual(d1[5],['90', 5])
        self.assertEqual(d1[6],['同桌', 6])
        self.assertEqual(d1[7],['绅士', 7])
        self.assertEqual(d1[8],['喜欢炫耀', 8])
        self.assertEqual(d1[9],['阔少爷', 9])

    def test_dirdictfile(self):
        f = Dictionary("SAKURO")
        d = f.read("NAME")
        d1 = DynArray()
        n = 0
        
        for i in d:
            if type(i) == list:
                for v in i:
                    if type(v) == list:
                        for sv in v:
                            d1.insert(n,[sv,n])
                            n=n+1                            
                    else:
                        d1.insert(n,[v,n])
                        n=n+1                        
            else:
                d1.insert(n,[i,n])
                n=n+1

        f.close()  
#         print(d1.list)
        self.assertEqual(d1[0],['D', 0])
        self.assertEqual(d1[1],['1', 1])
        self.assertEqual(d1[2],['', 2])
        self.assertEqual(d1[3],['姓名', 3])
        self.assertEqual(d1[4],['10L', 4])
        self.assertEqual(d1[5],['S', 5])
        self.assertEqual(d1[6],['', 6])

    def test_to_list(self):
        f = File("MOVIES")
        d = f.read(1) 
        t = d.list
        self.assertEqual(t, ['中国', '活着', '巩俐', '葛优', 'UNKNOWN', '1994/1/1', '一部讲述苦难的电影', '13512345678'])
        f.close()

        f = Dictionary("MOVIES")
        d = f.read("@ID")
        t = d.list
        self.assertEqual(t, ['D', '0', '', 'MOVIES', '10L', 'S', '', ''])
        f.close()

        with File("SAKURO") as sf:
            d = sf.read(5)
            t = d.list
            self.assertEqual(t, ['樱杏子', 'girl', '12', '小学六年级学生', '98', '100', '姐姐', ['成绩好', '懂事']])

        with Dictionary("SAKURO") as df:
            d = df.read("NAME")
            t = d.list
            self.assertEqual(t, ['D', '1', '', '姓名', '10L', 'S', ''])
            f.close()

        d = DynArray()
        d.insert(1,"a")
        d.insert(2,"b")
        d.insert(3,"c")
        t = d.list
        self.assertEqual(t, ['a', 'b', 'c'])

        d = DynArray()
        d.insert(1,"@")
        d.insert(2,"#")
        d.insert(3,"$")
        t = d.list
        self.assertEqual(t, ['@', '#', '$'])

        d1 = DynArray()
        t1 = d1.list
        self.assertEqual(t1,[])
        d2 = DynArray()
        d2.insert(1,"a")
        d2.insert(2,"b")
        d2.insert(3,"c")
        t2 = d2.list
        t = t1 + t2
        self.assertEqual(t,['a', 'b', 'c'])

        d = DynArray()
        n = 1
        for i in range(0,1000):
            d.insert(n,i)
            n = n + 1
        t=d.list
        self.assertEqual(t[1:2],[1])  

        #Error
        self.assertRaises(TypeError, d.list,1)        
        #Error:argument 2 must be str, not int
        self.assertRaises(TypeError, d.list," ",1)
        #Error:function takes at most 2 arguments (3 given)
        self.assertRaises(TypeError, d.list,"a","b","x")
        #Error:Required argument 'replacewith' (pos 2) not found
        self.assertRaises(TypeError, d.list,"a") 
                                                                
if __name__ == '__main__':
    unittest.main()
