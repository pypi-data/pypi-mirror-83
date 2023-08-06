from pkg_resources import get_distribution, DistributionNotFound

from km3services.core import oscillationprobabilities

version = get_distribution(__name__).version
