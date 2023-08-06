from pkg_resources import get_distribution, DistributionNotFound

version = get_distribution(__name__).version


import km3services.oscprob
