#pragma once

#include <cstddef>
#include <vector>
#include <unordered_map>
#include "platform.h"
#include "mocosMath.h"

class Sampler final
{
    const std::vector<double>& probabilities;
    size_t idx;
    size_t to_sample_left;
    const double precision;
    const double beta_bias;
    double confs_prob;
    double chasing_prob;
    size_t current_count;

 public:
    Sampler(const std::vector<double>& probabilities, size_t to_sample, double precalculated_sum = 0.0, double beta_bias = 5.0);

    MOCOS_FORCE_INLINE size_t count() const { return current_count; };

    MOCOS_FORCE_INLINE size_t index() const { return idx; };

    bool advanceToNextConfiguration();
};


class NonReplacingSampler final
{
    const size_t n;
    size_t last_idx;
    std::unordered_map<size_t, size_t> replacements;

    MOCOS_FORCE_INLINE size_t get(size_t idx) { return replacements.count(idx) > 0 ? replacements[idx] : idx; };
    MOCOS_FORCE_INLINE size_t set(size_t idx, size_t towhat) { return replacements[idx] = get(towhat); };

 public:
    NonReplacingSampler(size_t _n);

    size_t next();
};

std::vector<size_t> ShuffledSample(const std::vector<double>& probabilities, size_t to_sample);
