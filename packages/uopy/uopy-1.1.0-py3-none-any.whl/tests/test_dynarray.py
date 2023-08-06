# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

import unittest
from tests.unitestbase import UniTestBase
from uopy import DynArray


class TestDynArray(UniTestBase):

    def test_garbage_data(self):
        l = [123, [[[[[1, 2, 'abc']], ['def'], 'v2']]]]
        d = DynArray(l)
        self.assertEqual(d, DynArray(b"123\xfe[[1, 2, 'abc']]\xfb['def']\xfbv2"))
        self.assertEqual(d, b"123\xfe[[1, 2, 'abc']]\xfb['def']\xfbv2")
        self.assertEqual(b"123\xfe[[1, 2, 'abc']]\xfb['def']\xfbv2", d)
        self.assertEqual(d, l)
        self.assertEqual(l, d)
        self.assertTrue(l == d)
        self.assertTrue(d == l)

    def test_list_ops(self):
        d = DynArray(DynArray(b'v1\xfdv2\xfef2\xfesv1\xfcsv2'))
        d.insert(-1, -1)
        d.append(-2)
        d.extend({6: 7, 8: 9})
        self.assertEqual(len(d), 7)

        del d[0][0]
        self.assertEqual(d[0][0], 'v2')

        d.insert(2, "f3")
        d[2] = [d[2], 'v4']
        d1 = d.pop(4)
        self.assertEqual(d1, [['sv1', 'sv2']])

    def test_empty_dynarray(self):
        d = DynArray()
        d.append("F1")
        d.append([1, 2, 3])
        d.append(['a', 'b', 'c'])
        self.assertEqual(d, b'F1\xfe1\xfd2\xfd3\xfea\xfdb\xfdc')

    def test_scalar(self):
        d = DynArray([1, 2, [[3], 4]])
        d.make_nested_list(2)
        d[2][1].append(98)
        self.assertEqual(d, [1, 2, [[3], [4, 98]]])

        d = DynArray([""])
        d.make_list(0)
        d[0].append("1")
        self.assertEqual(d, [['', '1']] )

        d = DynArray()
        d.append("1")
        self.assertEqual(d, 1)

    def test_iconv(self):
        a = DynArray('02-23-85')
        b = a.iconv('D')
        self.assertTrue(b == '6264')

    def test_oconv(self):
        a = DynArray(0)
        b = a.oconv('D')
        if self.session.db_type == "UD":
            self.assertFalse(b != '31 Dec 1967')
        else:
            self.assertFalse(b != '31 DEC 1967')

    def test_format(self):
        d = DynArray('236986')
        res = d.format('R##-##-##')
        self.assertTrue(res == '23-69-86')


if __name__ == '__main__':
    unittest.main()
