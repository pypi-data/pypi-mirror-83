# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

import unittest
import uopy
from uopy import EXEC_REPLY, Command, File, UOError

class UniTestBaseCn(unittest.TestCase):
    config = {
        'user': 'qa',
        'password': 'no1wayQA',
        # "service": 'uvcs',
        # 'account': 'XDEMO'
        # "service" : 'udcs',
        # 'account': 'c:/u2/ud82/XDEMO'
    }

    def setUp(self):
        self.config = UniTestBaseCn.config
        self.session = uopy.connect(**self.config)

    def tearDown(self):
        self.session.close()

    def get_session(self):
        self.config = UniTestBaseCn.config
        return uopy.connect(**self.config)

    def create_test_file3(self, filename):
        cmd = Command()
        try:
            file = File(filename)
            file.close()
            self.delete_test_file(filename)
        except:
            pass
        finally:
            # create the file
            if self.session.db_type == "UV":
                cmd.command_text = "CREATE.FILE {} 18 15 2".format(filename)
            else:
                cmd.command_text = "CREATE.FILE {} 1".format(filename)

            cmd.run()
            while cmd.status == EXEC_REPLY:
                cmd.reply(filename)

    def create_test_file30(self, filename):
        cmd = Command()
        try:
            file = File(filename)
            file.close()
            self.delete_test_file(filename)
        except:
            pass
        finally:
            # create the file
            if self.session.db_type == "UV":
                cmd.command_text = "CREATE.FILE {} 30".format(filename)
            else:
                cmd.command_text = "CREATE.FILE {} 1".format(filename)

            cmd.run()
            while cmd.status == EXEC_REPLY:
                cmd.reply(filename)

    def delete_test_file(self, filename):
        cmd = Command()
        cmd.command_text = "DELETE.FILE {}".format(filename)

        if self.session.db_type == "UD":
            cmd.command_text += " FORCE";

        cmd.run()
        if cmd._status == EXEC_REPLY:
            cmd.reply("Y")

    def create_test_index_file(self, filename, field):
        self.delete_test_index_file(filename, field)
        cmd = Command()
        cmd.command_text = "CREATE.INDEX {} {}".format(filename, field)
        cmd.run()
        while cmd.status == EXEC_REPLY:
            cmd.reply("")

        cmd.command_text = "BUILD.INDEX {} {}".format(filename, field)
        cmd.run()

    def delete_test_index_file(self, filename, field):
        cmd = Command()
        cmd.command_text = "DELETE.INDEX {} {}".format(filename, field)
        cmd.run()
        while cmd.status == EXEC_REPLY:
            cmd.reply("Y")
    
    # Create the static file
    def CreateFile3(self,fn):
        cmd = Command()
        try:
            file = File(fn)
            file.close()
            self.delete_test_file(fn)
        except:
            pass
        finally:
            # create the file
            if self.session.db_type == "UV":
                cmd.command_text = "CREATE.FILE {} 4 3 1".format(fn)
                
            else:
                cmd.command_text = "CREATE.FILE {} 1".format(fn)

            cmd.run()
            while cmd.status == EXEC_REPLY:
                cmd.reply(fn)
            
                        