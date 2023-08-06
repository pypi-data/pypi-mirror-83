# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

from uopy import UOError, EXEC_MORE_OUTPUT, SequentialFile, Command
from tests.unitestbase import *


class TestCommand(UniTestBase):
    session = None

    @classmethod
    def setUpClass(cls):

        try:
            config = UniTestBase.config
            TestCommand.session = uopy.connect(**config)

            subroutine = """
            CRT "THIS IS TEST COMMAND TEST SUITE"
            INPUT ANS
            CRT ANS
            
            """
            seq_file = SequentialFile('BP', 'TEST_COMMAND', True)
            seq_file.write_block(subroutine)
            seq_file.close()

            cmd = Command()
            cmd.command_text = "BASIC BP TEST_COMMAND"
            cmd.run()

            cmd.command_text = "CATALOG BP TEST_COMMAND"
            cmd.run()
            if cmd.status == uopy.EXEC_REPLY:
                cmd.reply("Y")
        except Exception as e:
            raise
        finally:
            if TestCommand.session:
                TestCommand.session.close()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_cancel(self):
        cmd = Command()
        cmd.command_text = "RUN BP TEST_COMMAND"
        cmd.run()
        cmd.cancel()
        self.assertRaises(UOError, cmd.reply, "Hello World!")

    def test_next_response(self):
        cmd = Command()
        cmd.command_text = "LIST VOC"
        cmd.buffer_size = 200
        cmd.run()
        while cmd.status == EXEC_MORE_OUTPUT:
            cmd.next_response()
        self.assertEqual(cmd.status, uopy.EXEC_COMPLETE)

    def test_buffer_size(self):
        cmd = Command()
        cmd.buffer_size = 10
        cmd.command_text = 'RUN BP TEST_COMMAND'
        cmd.run()
        self.assertEqual(cmd.response, 'THIS IS TE')

    def test_reply(self):
        cmd = Command()
        cmd.command_text = "RUN BP TEST_COMMAND"
        cmd.run()
        cmd.reply("Hello World!")
        self.assertIn('Hello World!\r\nHello World!\r\n', cmd.response)

    def test_run(self):
        cmd = Command("COUNT VOC")
        cmd.run()
        self.assertTrue(True)

    def notest_AE(self):
        cmd = Command()
        cmd.command_text = "ED VOC MOVIES_2"
        cmd.run()
        if cmd.status == uopy.EXEC_REPLY:
            # cmd.reply("I\nPA\nLIST MOVIES 2\n\nFI\n")
            cmd.reply("I")
            cmd.reply("\n")
            cmd.reply("PA")
            cmd.reply("\n")
            cmd.reply("LIST MOVIES 2")
            cmd.reply("\n")
            cmd.reply("\n")
            cmd.reply("FI")
            cmd.reply("\n")


        self.assertEqual(0, cmd.at_system_return_code)

        cmd = Command()
        cmd.command_text = "MOVIES_2"
        cmd.run()
        self.assertIn("1 records listed", cmd.response)


if __name__ == '__main__':
    unittest.main()
