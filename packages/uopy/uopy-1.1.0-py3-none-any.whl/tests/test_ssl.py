# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

import unittest

import uopy
from tests.unitestbase import UniTestBase
from uopy import Command


@unittest.skipIf(uopy.config.connection["ssl"], "SSL is turned on by default, no need to test it individually.")
@unittest.skipIf(uopy.config.pooling["pooling_on"], "Pooling must be off to run this test.")
class TestSsl(UniTestBase):

    def test_ssl(self):
        with uopy.connect(ssl=True, **self.config) as session:
            command_text = 'LIST VOC'
            cmd = Command(command_text)
            cmd.run()
            self.assertTrue("LIST" in cmd.response[0:len(command_text)])
