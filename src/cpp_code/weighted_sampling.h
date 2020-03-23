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
    Sampler(const std::vector<double>& probabilities, size_t to_sample, double precision = 1.0, double beta_bias = 5.0);

    MOCOS_FORCE_INLINE size_t count() const { return current_count; };

    MOCOS_FORCE_INLINE size_t index() const { return idx; };

    MOCOS_FORCE_INLINE bool advanceToNextConfiguration()
    #if !MOCOS_HIDE_IMPLEMENTATIONS
    {
        /* This function will be used mainly in very small, tight loops, therefore it makes sense to
         * aggressively inline it, despite its seemingly large body.
         */
        while(true)
        {
            double curr_conf_prob_left, current_prob;

            if(to_sample_left <= 0)
                return false;

            if(confs_prob < chasing_prob)
            {
                // Beta was last
                current_count = 1;
                to_sample_left--;
                idx++;
                current_prob = probabilities[idx];
                confs_prob += current_prob;
                while(confs_prob <= chasing_prob)
                {
                    idx++;
                    current_prob = probabilities[idx];
                    confs_prob += current_prob;
                }
                if(to_sample_left <= 0)
                    return true;
                curr_conf_prob_left = confs_prob - chasing_prob;
            }
            else
            {
                // Binomial was last
                current_count = 0;
                idx++;
                current_prob = probabilities[idx];
                confs_prob += current_prob;
                curr_conf_prob_left = current_prob;
            }

            double prob_left_to_1 = precision - chasing_prob;
            double expected_confs = curr_conf_prob_left * to_sample_left / prob_left_to_1;

            if(expected_confs <= beta_bias)
            {
                // Beta mode: we keep making beta jumps until we leave the current configuration
                chasing_prob += rdvariate_beta_1_b(to_sample_left) * prob_left_to_1;
                while(chasing_prob <= confs_prob)
                {
                    current_count++;
                    to_sample_left--;
                    if(to_sample_left == 0)
                        return true;
                    prob_left_to_1 = precision - chasing_prob;
                    chasing_prob += rdvariate_beta_1_b(to_sample_left) * prob_left_to_1;
                }
                if(current_count > 0)
                    return true;
            }
            else
            {
                // Binomial mode: a single binomial step
                size_t rbin = rdvariate_binom(to_sample_left, curr_conf_prob_left/prob_left_to_1);
                current_count += rbin;
                to_sample_left -= rbin;
                chasing_prob = confs_prob;
                if(current_count > 0)
                    return true;
            }
        };
    }
    #else
    ;
    #endif
};
