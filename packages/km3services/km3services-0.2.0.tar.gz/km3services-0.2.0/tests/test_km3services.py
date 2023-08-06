#!/usr/bin/env python3

import unittest
import numpy as np

import km3services


class TestOscProb(unittest.TestCase):
    def test_oscillationprobabilities(self):
        n = 100
        energies = np.random.randint(1, 50, n)
        cos_zeniths = 1 - np.random.rand(n) * 2
        probabilities = km3services.oscprob.oscillationprobabilities(
            1, 1, energies, cos_zeniths
        )
        assert np.all(probabilities <= 1)
