# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

from uopy import SequentialFile, Command
from uopy import UOError
from tests.unitestbase import *


class TestSequentialFile(UniTestBase):

    def setUp(self):
        super().setUp()

        self.line1 = "This is a test of the emergency broadcast system"
        self.line2 = "This is only a test"
        self.line3 = "Had this been a real test, you would have been instructed"
        self.line4 = "To find shelter."
        self.block1 = "Let's form a block\nof data\nthat can" + " be written\n in multiple lines\n and" \
                      + " put into a file\n"

        with SequentialFile("BP", "UOPYTESTSEQ", True) as self.seq_file:
            self.seq_file.seek(0)
            self.seq_file.write_eof()
            self.seq_file.seek(0)
            self.seq_file.write_line(self.line1)
            self.seq_file.write_line(self.line2)
            self.seq_file.write_line(self.line3)
            self.seq_file.write_line(self.line4)
            self.seq_file.write_block(self.block1)

    def tearDown(self):
        cmd = Command()
        cmd.command_text = "DELETE BP UOPYTESTSEQ"
        cmd.run()
        super().tearDown()

    def test_read(self):
        seq_file = SequentialFile('BP', "UOPYTESTSEQ")
        line1 = seq_file.read_line()
        line2 = seq_file.read_line()
        line3 = seq_file.read_line()
        line4 = seq_file.read_line()
        blk = seq_file.read_block()
        self.assertEqual(line1, self.line1)
        self.assertEqual(line2, self.line2)
        self.assertEqual(line3, self.line3)
        self.assertEqual(line4, self.line4)
        self.assertEqual(self.session.decode(blk), self.block1)
        seq_file.close()

    def test_seek(self):
        with SequentialFile('BP', "UOPYTESTSEQ") as seq_file:
            seq_file.seek(0)
            seq_file.block_size = 6
            blk_data = seq_file.read_block()
            self.assertEqual(self.session.decode(blk_data), "This i")

            seq_file.seek(25)
            blk_data = seq_file.read_line()
            self.assertEqual(self.session.decode(blk_data)[:6], "rgency")

            seq_file.seek(-10, 2)
            seq_file.block_size = 1024
            blk_data = seq_file.read_block()
            self.assertEqual(self.session.decode(blk_data), "to a file\n")
            self.assertEqual(seq_file.status, 0)

            blk_data = seq_file.read_block()
            self.assertEqual(self.session.decode(blk_data), "")
            self.assertEqual(seq_file.status, 1)


if __name__ == '__main__':
    try:
        unittest.main()
    except Exception as e:
        raise UOError(message=str(e))
