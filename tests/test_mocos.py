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

def check_distributions(f1, f2, argss):
    for args in argss:
        for _ in range(10):
            x = scipy.stats.ks_2samp(list(f1(*args)), list(f2(*args)))
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

check_distributions(d1, d2, args)




print("All seems OK!")

