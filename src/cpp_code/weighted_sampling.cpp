#include "weighted_sampling.h"

Sampler::Sampler(const std::vector<double>& _probabilities, size_t to_sample, double _precision, double _beta_bias) :
probabilities(_probabilities),
idx(-1),
to_sample_left(to_sample),
precision(_precision),
beta_bias(_beta_bias),
confs_prob(0.0),
chasing_prob(0.0)
{}
