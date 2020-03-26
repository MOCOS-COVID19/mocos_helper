import pkg_resources
import cppyy

import platform

if False:
    cppyy.cppdef(
    """
    #define MOCOS_CPPYY
    #include "{0}"
    """.format(
    pkg_resources.resource_filename("mocos_helper", "cpp_code/weighted_sampling.h"),
    ))

    cppyy.load_library(pkg_resources.resource_filename("mocos_helper", "cpp_code/libMocosHelper.so"))
else:
    cppyy.cppdef("""#include "{0}" """.format(pkg_resources.resource_filename("mocos_helper", "cpp_code/unity_build.cpp")))

from cppyy.gbl import Sampler, std, ShuffledSample, mocos_seed, rand_stdunif, rand_lognormal, rand_exponential_beta, rand_poisson, \
                      rand_uniform, NonReplacingSampler, OnesVector, rand_gamma
from cppyy.gbl import randint as cpp_randint
from cppyy.gbl import rand_lognormal as cpp_lognormal

def seed(seed):
    mocos_seed(int(seed))

def randint(a, b):
    return cpp_randint(a, b)

def rand():
    return rand_stdunif()

def lognormal(mean, sigma):
    return rand_lognormal(mean, sigma)

def exponential(scale):
    # Following Numpy's parametrization by beta = 1.0/lambda
    return rand_exponential_beta(scale)

def gamma(alpha, beta):
    return rand_gamma(alpha, beta)

def poisson(lam):
    return rand_poisson(lam)

def uniform(low, high):
    return rand_uniform(low, high)

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

def sample_idxes_with_replacement_uniform(idx_range, to_sample):
    V = OnesVector(idx_range)

    S = Sampler(V, to_sample, float(idx_range))

    while S.advanceToNextConfiguration():
        yield S.index()

def sample_with_replacement_shuffled(weights, to_sample):
    if type(weights) != std.vector("double"):
        weights = std.vector("double")(weights)

    return ShuffledSample(weights, to_sample)


def sample_set(items, weights, to_sample):
    if type(weights) != std.vector("double"):
        weights = std.vector("double")(weights)
    sampler = Sampler(weights, to_sample)

    while sampler.advanceToNextConfiguration():
        what = items[sampler.index()]
        for _ in range(sampler.count()):
            yield what

def randomly_split_list(L, howmuch):
    '''Randomly splits L into two sublists, second containing howmuch elements,
    and the first one the rest.

    L is consumed in the process. The elements are placed on their lists in
    undefined order.

    Example: split_list([1,2,3,4,5,6,7,8,9,10], 3) may return:
    ([8,1,2,10,9,5,4], [6,3,7])
    '''
    inverse = False
    if len(L)/2 < howmuch:
        inverse = True
        howmuch = len(L) - howmuch
        assert howmuch >= 0

    ret = []
    for _ in range(howmuch):
        idx = randint(0, len(L)-1)
        ret.append(L[idx])
        L[idx] = L[-1]
        L.pop()

    if inverse:
        return ret, L
    else:
        return L, ret

def nonreplace_sample(iterable, howmany):
    '''Perform sampling without replacement from iterable. Number of selected
    elements is min(len(iterable), howmany). Example:

    nonreplace_sample(range(10), 5) may return:
    [4, 7, 2, 1, 9]

    Runs in O(len(iterable)), so use this function only when len(iterable) is 
    comparable to howmany, and nonreplace_sample_few otherwise. Unlike
    nonreplace_sample_few this function can accept a generator.'''

    ret = []
    iterator = iterable.__iter__()
    try:
        while len(ret) < howmany:
            ret.append(next(iterator))
    except StopIteration:
        return ret


    try:
        while True:
            x = next(iterator)
            idx = randint(0, howmany)
            if idx < len(ret):
                ret[idx] = x
            howmany += 1
    except StopIteration:
        return ret

def nonreplace_sample_few(indexable, howmany, avoid = None):
    '''Perform sampling without replacement from iterable. Number of selected
    elements is howmany, and will throw IndexError if howmany > len(indexable).

    nonreplace_sample(list(range(10)), 5) may return:
    [4, 7, 2, 1, 9]

    Runs in O(howmany), and is preferable to nonreplace_sample unless you have
    a generator that you need to sample from.
    '''
    ret = []
    N = len(indexable)
    NRS = NonReplacingSampler(N)
    while len(ret) < howmany:
        X = indexable[NRS.next()]
        if X != avoid:
            ret.append(X)
    return ret

if __name__ == "__main__":
    # Example usage
    for idx, count in sample_with_replacement([0.3, 0.2, 0.5], 100):
        print("Index:", idx, "selected", count, "times.")
