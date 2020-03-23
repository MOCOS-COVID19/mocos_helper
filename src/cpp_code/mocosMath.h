#include <random>

extern std::mt19937 random_gen;
extern std::uniform_real_distribution<double> stdunif;

inline double rdvariate_beta_1_b(double b, std::mt19937& rgen = random_gen)
{
    return 1.0 - pow(stdunif(rgen), 1.0/b);
}

#include "btrd.h"

inline size_t rdvariate_binom(size_t tries, double succ_prob, std::mt19937& rgen = random_gen)
{
    if (succ_prob >= 1.0)
        return tries;
    return boost_binomial_distribution_variate(tries, succ_prob, rgen);
}

void mocos_seed(std::mt19937::result_type seed);
