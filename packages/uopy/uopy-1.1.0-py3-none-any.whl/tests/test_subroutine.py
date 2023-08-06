# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

from uopy import Subroutine, SequentialFile, Command, DynArray, UOError
from tests.unitestbase import *


class TestSubroutine(UniTestBase):

    def setUp(self):
        super().setUp()
        subroutine = """
        SUBROUTINE SUBTEST (ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7)
            ARG2 = ARG3
            ARG1 = "It worked"
            ARG3 = 0
            ARG4 = (ARG5+ARG6) * ARG7
            RETURN
        END
        """

        seq_file = SequentialFile('BP', 'SUBTEST', True)
        seq_file.write_block(subroutine)
        seq_file.close()

        cmd = Command()
        cmd.command_text = "BASIC BP SUBTEST"
        cmd.run()

        cmd.command_text = "CATALOG BP SUBTEST"
        cmd.run()

        if cmd.status == uopy.EXEC_REPLY:
            cmd.reply("Y")

    def tearDown(self):
        super().tearDown()

    def test_call(self):
        dyn_array = DynArray(["Meeks", ['1', '2'], "Merry"])
        sub = Subroutine("SUBTEST", 7)
        sub.args[0] = "David"
        sub.args[1] = "Thomas"
        sub.args[2] = ["Meeks", ['1', '2'], "Merry"]
        sub.args[3] = "95"
        sub.args[4] = "15"
        sub.args[5] = "92"
        sub.args[6] = "-6"

        sub.call()

        # results = list(map(lambda idx: sub.args[idx], range(0, 7)))
        self.assertEqual(sub.args[0], "It worked")
        self.assertEqual(sub.args[1], dyn_array)
        self.assertEqual(sub.args[2], "0")
        self.assertEqual(sub.args[3], -642)
        self.assertEqual(sub.args[4], "15")
        self.assertEqual(sub.args[5], "92")
        self.assertEqual(sub.args[6], "-6")

    def test_call_error(self):
        sub = Subroutine()
        with self.assertRaises(IndexError):
            sub.args[0] = "a"
        self.assertRaises(UOError, sub.call)

    def test_large_parameters(self):
        sub = Subroutine("SUBTEST", 7)
        sub.args[0] = "0123456789" * 2 ** 5
        sub.args[1] = "~!@$%^&*()" * 2 ** 10
        sub.args[2] = "abcdefgijk" * 2 ** 20
        sub.args[3] = "95"
        sub.args[4] = "15"
        sub.args[5] = "92"
        sub.args[6] = "-6"

        sub.call()

        self.assertEqual(sub.args[3], -642)
        self.assertEqual(sub.args[6], "-6")


if __name__ == '__main__':
    unittest.main()
