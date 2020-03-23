class Sampler
{
    IsoLayeredGenerator ILG;
    size_t to_sample_left;
    const double precision;
    const double beta_bias;
    double confs_prob;
    double chasing_prob;
    size_t current_count;

 public:
    IsoStochasticGenerator(Iso&& iso, size_t no_molecules, double precision = 0.9999, double beta_bias = 5.0);

    ISOSPEC_FORCE_INLINE size_t count() const { return current_count; };

    ISOSPEC_FORCE_INLINE double mass() const override final { return ILG.mass(); };

    ISOSPEC_FORCE_INLINE double prob() const override final { return static_cast<double>(count()); };

    ISOSPEC_FORCE_INLINE double lprob() const override final { return log(prob()); };

    ISOSPEC_FORCE_INLINE void get_conf_signature(int* space) const override final { ILG.get_conf_signature(space); };

    ISOSPEC_FORCE_INLINE bool advanceToNextConfiguration() override final
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
                ILG.advanceToNextConfiguration();
                current_prob = ILG.prob();
                confs_prob += current_prob;
                while(confs_prob <= chasing_prob)
                {
                    ILG.advanceToNextConfiguration();
                    current_prob = ILG.prob();
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
                ILG.advanceToNextConfiguration();
                current_prob = ILG.prob();
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
};
