# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

import unittest
import uopy
from uopy import EXEC_REPLY, Command, File, UOError


class UniTestBase(unittest.TestCase):
    config = {
        'user': 'jmao',
        'password': 'u2',
        # 'max_pool_size': 2
        # "service": 'uvcs',
        # 'account': 'XDEMO'
        # "service" : 'udcs',
        # 'account': 'c:/u2/ud82/XDEMO'
    }

    def setUp(self):
        self.config = UniTestBase.config
        self.session = uopy.connect(**self.config)

    def tearDown(self):
        self.session.close()

    def get_session(self):
        self.config = UniTestBase.config
        return uopy.connect(**self.config)

    def create_test_file(self, filename):
        cmd = Command()
        try:
            test_file = File(filename)
            test_file.close()
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
