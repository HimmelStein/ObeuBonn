# -*- coding: utf-8 -*-

from context import ObeuBonn
import unittest
import os


class Test_functions_in_read_xls(unittest.TestCase):
    """Basic tests cases."""

    def test_xls_tables(self):
        fpath = os.path.abspath('./data')
        tbls = ObeuBonn.xls_tables(fpath)
        print(fpath)
        assert len(tbls) == 5


if __name__ == '__main__':
    unittest.main()