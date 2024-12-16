import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from interaction_matrix.finely_structured_random_matrix import \
fs_statistics, fsrm_instance, ust_to_mu_sigma_gamma, mu_sigma_gamma_to_ust, elliptical_instance