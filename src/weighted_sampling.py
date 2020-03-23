import pkg_resources
import cppyy

cppyy.cppdef(
"""
#define MOCOS_CPPYY
#include "{0}"
#include "{1}"
""".format(
pkg_resources.resource_filename("mocos_helper", "cpp_code/weighted_sampling.h"),
pkg_resources.resource_filename("mocos_helper", "cpp_code/mocosMath.h")
))

cppyy.load_library(pkg_resources.resource_filename("mocos_helper", "cpp_code/libMocosHelper.so"))

from cppyy.gbl import Sampler, std

def sample_with_replacement(weights, to_sample):
    '''Weighted sampling with replacement

    Given an interable (preferably cppyy's std.vector<double>, others will be converted)
    samples to_sample indexes, according to the weights. Weights are proportional, 
    and need not sum to 1.

    Returns list of tuples: (index, number if times selected)

    For example:

    sample_with_replacement([0.0001, 0.9, 0.1, 0.000001], 100) might produce:
    [(1, 91), (2, 9)]
    '''

    if type(weights) != std.vector("double"):
        weights = std.vector("double")(weights)
    sampler = Sampler(weights, to_sample)
    while sampler.advanceToNextConfiguration():
        yield (sampler.index(), sampler.count())


if __name__ == "__main__":
    # Example usage
    for idx, count in sample_with_replacement([0.3, 0.2, 0.5], 100):
        print("Index:", idx, "selected", count, "times.")
