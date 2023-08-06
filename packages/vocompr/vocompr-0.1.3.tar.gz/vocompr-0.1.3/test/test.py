import random
import sys
import unittest

from vocompr import *


class Test(unittest.TestCase):
    def test_identity(self):
        s = "Hello World!"
        assert (s == unvocompr(vocompr(s)))

    def test_compression_rate_on_binary_data(self):
        to_write = ""
        for _ in range(100000):
            to_write += str(random.randint(0, 1))
        assert (compression_rate(to_write) < 0.13)
