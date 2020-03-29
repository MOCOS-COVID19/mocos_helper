import mocos_helper as MH




S = list(MH.sample_with_replacement([0.2, 0.6, 0.7, 0.3], 300))
assert sum(x[1] for x in S) == 300

L = list(range(100))

L1, L2 = MH.randomly_split_list(L, 30)

assert len(L1) == 70
assert len(L2) == 30

assert sorted(L1+L2) == list(range(100))

S = list(MH.nonreplace_sample(range(100), 30))
assert len(S) == 30
assert len(set(S)) == 30
assert set(S).issubset(set(range(100)))

S = MH.sample_with_replacement_shuffled([0.2, 0.6, 0.7, 0.3], 300)

assert MH.randint(30, 70) in range(30, 71)

assert 0.0 <= MH.rand() <= 1.0

MH.lognormal(0.0, 1.0)
MH.exponential(1.0)

assert 0 <= MH.poisson(7.0)

assert 3.7 <= MH.uniform(3.7, 5.6) <= 5.6

S = list(MH.sample_idxes_with_replacement_uniform(1000, 1003))
assert len(S) == len(set(S))
assert set(S).issubset(set(range(1000)))



import scipy.stats
import numpy.random
import random

def check_distributions(f1, f2, argss, same_length = True):
    for args in argss:
        for _ in range(10):
            L1 = list(f1(*args))
            L2 = list(f2(*args))
            if same_length:
                assert len(L1) == len(L2)
            x = scipy.stats.ks_2samp(L1, L2)
            print(x.pvalue)
            assert x.pvalue > 0.0005


def unpack_sample(L):
    ret = []
    for x, cnt in L:
        for _ in range(cnt):
            ret.append(x)
    return ret

d1 = lambda probs, size: unpack_sample(MH.sample_with_replacement(probs, size))
d2 = lambda probs, size: numpy.random.choice(len(probs), size = size, p = probs)


def const_list(length):
    return [1.0/length] * length

plist = [float(x) for x in range(1000)]
s = sum(plist)
plist = [x/s for x in plist]
args = [([0.01]*100, 300), ([0.01]*100, 20), ([0.01]*100, 30000), (plist, 10), (plist, 1000), (plist, 100000)]

check_distributions(d1, d2, args)

d1 = lambda probs, size: MH.sample_with_replacement_shuffled(probs, size)

check_distributions(d1, d2, args)

d1 = lambda idx_range, to_sample: list(MH.sample_idxes_with_replacement_uniform(len(idx_range), to_sample))
d2 = lambda idx_range, to_sample: numpy.random.choice(list(range(len(idx_range))), size=to_sample)

check_distributions(d1, d2, args, same_length = False)

d1 = lambda idx_range, to_sample: list(MH.sample_idxes_with_replacement_uniform(len(idx_range), to_sample))
d2 = lambda idx_range, to_sample: set(numpy.random.choice(list(range(len(idx_range))), size=to_sample))

check_distributions(d1, d2, args, same_length = False)

d1 = lambda probs, to_sample: list(MH.sample_set(list(range(len(probs))), probs, to_sample))
d2 = lambda probs, to_sample: numpy.random.choice(list(range(len(probs))), p = probs, size=to_sample)

check_distributions(d1, d2, args)

args = [([0.0001]*10000, 300), ([0.0001]*10000, 20), ([0.0001]*10000, 8000), (plist, 10), (plist, 100), (plist, 700)]

d1 = lambda probs, to_sample: MH.nonreplace_sample(list(range(len(probs))), to_sample)
d2 = lambda probs, to_sample: numpy.random.choice(list(range(len(probs))), size=to_sample, replace=False)

check_distributions(d1, d2, args)

d1 = lambda probs, to_sample: MH.nonreplace_sample_few(list(range(len(probs))), to_sample)
d2 = lambda probs, to_sample: numpy.random.choice(list(range(len(probs))), size=to_sample, replace=False)

check_distributions(d1, d2, args)

d1 = lambda probs, to_sample: MH.randomly_split_list(list(range(len(probs))), to_sample)[1]
d2 = lambda probs, to_sample: numpy.random.choice(list(range(len(probs))), size=to_sample, replace=False)

check_distributions(d1, d2, args)

d1 = lambda probs, to_sample: MH.randomly_split_list(list(range(len(probs))), to_sample)[0]
d2 = lambda probs, to_sample: numpy.random.choice(list(range(len(probs))), size=len(probs) - to_sample, replace=False)

check_distributions(d1, d2, args)

print("Checking random variate generators")

def check_rgvs(rvg1, rvg2, argss):
    for args in argss:
        for _ in range(10):
            L1 = [rvg1(*args) for _ in range(10000)]
            L2 = [rvg2(*args) for _ in range(10000)]
            x = scipy.stats.ks_2samp(L1, L2)
            print(x.pvalue)
            assert x.pvalue > 0.0005


args = [()]

d1 = MH.rand
d2 = random.random

args = [(0.0, 1.0), (0.3, 17.5), (1000.0, 1000000.0)]

d1 = MH.uniform
d2 = random.uniform

check_rgvs(d1, d2, args)

args = [(0.0, 1.0), (0.3, 17.5), (10.0, 0.3), (10.0, 20.0)]

d1 = MH.lognormal
d2 = numpy.random.lognormal

check_rgvs(d1, d2, args)

d1 = MH.exponential
d2 = numpy.random.exponential

check_rgvs(d1, d2, [(x[1],) for x in args])

d1 = MH.gamma
d2 = numpy.random.gamma

check_rgvs(d1, d2, args)

d1 = MH.poisson
d2 = numpy.random.poisson

check_rgvs(d1, d2, [(x[1],) for x in args])

print("Checking scipy distributions")

def check_rgvs_scipy(rvg1, rvg2, argss):
    for args in argss:
        for _ in range(10):
            L1 = [rvg1(*args) for _ in range(10000)]
            scipy_rvg = rvg2(a = args[0], loc = 0.0, scale = args[1])
            L2 = scipy_rvg.rvs(size=10000)
            x = scipy.stats.ks_2samp(L1, L2)
            print(x.pvalue)
            assert x.pvalue > 0.0005

args = [(0.1, 1.0), (0.3, 17.5), (10.0, 0.3), (10.0, 20.0)]

d1 = MH.gamma
d2 = scipy.stats.gamma

check_rgvs_scipy(d1, d2, args)

from math import log

def check_rgvs_scipy(rvg1, rvg2, argss):
    for args in argss:
        scale = args[0]
        logscale = log(scale)
        sigma = args[1]
        for _ in range(10):
            L1 = [rvg1(mean=logscale, sigma=sigma) for _ in range(10000)]
            scipy_rvg = rvg2(sigma, loc = 0.0, scale = scale)
            L2 = scipy_rvg.rvs(size=10000)
            x = scipy.stats.ks_2samp(L1, L2)
            print(x.pvalue)
            assert x.pvalue > 0.0005

d1 = MH.lognormal
d2 = scipy.stats.lognorm

check_rgvs_scipy(d1, d2, args)

L = list(range(10))
print(MH.extract_random(L))
print(L)

print("All seems OK!")

