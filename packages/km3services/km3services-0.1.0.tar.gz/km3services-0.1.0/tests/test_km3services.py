#!/usr/bin/env python3

import unittest

import km3services


class TestDummy(unittest.TestCase):
    def test_dummy(self):
        n = km3services.oscillationprobabilities({"energy": 1, "zenith": 123})
        assert float(n) <= 1
