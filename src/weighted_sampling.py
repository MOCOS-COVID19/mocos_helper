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

def sample_with_replacement(probabilities, to_sample):
    if type(probabilities) != std.vector("double"):
        probabilities = std.vector("double")(probabilities)
    sampler = Sampler(probabilities, to_sample)
    while sampler.advanceToNextConfiguration():
        yield (sampler.index(), sampler.count())


if __name__ == "__main__":
    # Example usage
    for idx, count in sample_with_replacement([0.3, 0.2, 0.5], 100):
        print("Index:", idx, "selected", count, "times.")
