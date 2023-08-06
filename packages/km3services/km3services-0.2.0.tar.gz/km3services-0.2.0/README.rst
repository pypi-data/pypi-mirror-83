Microservices for KM3NeT
========================

.. image:: https://git.km3net.de/km3py/km3services/badges/master/pipeline.svg
    :target: https://git.km3net.de/km3py/km3services/pipelines

.. image:: https://git.km3net.de/km3py/km3services/badges/master/coverage.svg
    :target: https://tgal.pages.km3net.de/km3services/coverage

.. image:: https://examples.pages.km3net.de/km3badges/docs-latest-brightgreen.svg
    :target: https://tgal.pages.km3net.de/km3services

This Python package provides access to KM3NeT microservices. It's in an early development
stage and the API will likely change any until v1.0.0 is released.

Installation
------------

As usual, install with ``pip``::

  pip install km3services

Available Microservices
-----------------------

OscProb
~~~~~~~

The ``km3services.oscprob`` module wraps the ``OscProb`` package to calculate neutrino
oscillation probabilities. Here is an example how to calculate the transition
probabilities from muon to electron neutrino (the API will be polished soon):

.. code-block:: python3

  import km3services
  import numpy as np

  n = 1000
  energies = np.random.randint(1, 50, n)  # generate `n` energies between 1-50 GeV
  cos_zeniths = -np.random.rand(n) / 2
  flav_in = 0   # electron neutrino
  flav_out = 1  # muon neutrino

  probabilities = km3services.oscprob.oscillationprobabilities(flav_in, flav_out, energies, cos_zeniths)
  print(probabilities)

The returned ``probabilities`` is a numpy array::

 [4.20254330e-03 7.46278836e-05 6.18139696e-04 4.03814960e-03
 3.38002558e-03 3.33962606e-04 4.53159234e-02 5.03111960e-02
 ...
 2.23391190e-03 2.07540790e-03 6.71385177e-03 3.03348121e-02
 1.86633322e-02 4.81416626e-03 4.55362912e-05 3.59935810e-03]
