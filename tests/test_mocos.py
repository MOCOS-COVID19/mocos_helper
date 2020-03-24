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
print(list(S))
print("All seems OK!")

