# -*- coding: utf-8 -*-
"""

Created on Sun Oct 25 09:32:49 2020

Github: https://github.com/tjczec01

@author: Travis J Czechorski

E-mail: tjczec01@gmail.com

"""

from .context import chemsys, chemsystest

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(chemsys.gui())


if __name__ == '__main__':
    unittest.main()