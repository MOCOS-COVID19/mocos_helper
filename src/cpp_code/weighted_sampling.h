#pragma once

#include <cstddef>
#include <vector>
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
