import generalised_lotka_volterra.finely_structured_random_matrix as fs
from scipy.integrate import solve_ivp
from tqdm import tqdm
import numpy as np

SPECIES_EXTINCT_ABUNDANCE_THRESHOLD = 1e-5
T_MAX = 1000.0

def print_progress_wrapper(dynamical_system, pbar, state):
    def wrapped(t, X, *args):
        last_t, dt = state
        n = int((t - last_t)/dt)
        pbar.update(n)
        state[0] = last_t + dt * n

        return dynamical_system(t, X, *args)
    
    return wrapped


def _lotka_volterra(t, X, alpha, r=1):
    dxdt = X*(r - X + alpha @ X)

    return dxdt

def interaction_matrix(mu_mat, sigma_mat, gamma_mat):
    return fs.fsrm_instance(mu_mat, sigma_mat, gamma_mat)

def interaction_matrices(mu_mat, sigma_mat, gamma_mat, number_of_matrices=1):
    N = len(mu_mat)
    matrices = np.zeros((number_of_matrices, N, N), dtype=float)
    for i in range(number_of_matrices):
        matrices[i] = interaction_matrix(mu_mat, sigma_mat, gamma_mat)

    return matrices

def run_dynamics(interaction_matrix, *, r=1, x0=None, T_max=T_MAX, print_progress=False, return_full_timeseries=False, **kwargs):
    '''
        x[i, t] = x_i(t)
        returns t, x
    '''

    if np.any(x0 == None):
        x0 = np.random.uniform(0, 1, interaction_matrix.shape[0])

    if len(np.shape(r)) == 1:
        r = r[:, np.newaxis]

    if print_progress:
        with tqdm(total=100, unit="‰") as pbar:
            sol = solve_ivp(print_progress_wrapper(_lotka_volterra, pbar, [0, T_max/100]), t_span=(0, T_max), y0=x0, args=(interaction_matrix, r), rtol=1e-5, vectorized=True, **kwargs)
    else:
        sol = solve_ivp(_lotka_volterra, t_span=(0, T_max), y0=x0, args=(interaction_matrix, r), rtol=1e-5, vectorized=True, **kwargs)

    if return_full_timeseries:
        return sol.t, sol.y
    
    return x_star(sol.y)

def iterate_dynamics(interaction_matrices, *, r_values=None, T_max=T_MAX, print_progress=False, **kwargs):
    '''
        returns x_star for each iteration x_star[i, j] = x_j at the ith iteration
        x[i] = x_star on the jth iteration
        only takes the final time step
    '''
    if np.any(r_values == None):
        r_values = np.ones(len(interaction_matrices))
    elif isinstance(r_values, (int, float)):
        r_values = np.ones(len(interaction_matrices))*r_values

    N = interaction_matrices[0].shape[0]
    iterations = len(interaction_matrices)
    x_star_mat = np.zeros((iterations, N))

    for i, (alpha, r) in tqdm(enumerate(zip(interaction_matrices, r_values)), disable=not print_progress):
        x = run_dynamics(alpha, r=r, T_max=T_max, **kwargs)
        x_star_mat[i, :] = x
    
    return x_star_mat

def N_star(x, *, min=SPECIES_EXTINCT_ABUNDANCE_THRESHOLD, max=np.inf):
    return np.sum(theta_star(x, min=min, max=max))
def x_star(x):
    '''
    returns the abundance of each species at the final time step,
    if the array is one dimensional, it does nothing, assuming that this is already equal to x_star
    '''
    if len(np.shape(x)) == 1:
        return x
    
    return x[:, -1]
def theta_star(x, *, min=SPECIES_EXTINCT_ABUNDANCE_THRESHOLD, max=np.inf):
    return (x > min) * (x < max)


def Mi(x):
    return np.average(x, axis=0)
def M(x):
    return np.average(x)


def qi(x):
    return np.average(x**2, axis=0)
def q(x):
    return np.average(x**2)


def phii(x, *, min=SPECIES_EXTINCT_ABUNDANCE_THRESHOLD, max=np.inf):
    return np.average((x > min) * (x < max), axis=0)
def phi(x, *, min=SPECIES_EXTINCT_ABUNDANCE_THRESHOLD, max=np.inf):
    return np.average(theta_star(x, min=min, max=max))


def reduced_interaction_matrix(x, alpha, *, min=SPECIES_EXTINCT_ABUNDANCE_THRESHOLD, max=np.inf, remove_dead_species=True):

    survivors = theta_star(x, min=min, max=max)
    if remove_dead_species:
        return alpha[survivors, :][:, survivors]
    return alpha*np.outer(survivors, survivors)

def survivors_mask(x, *, min1=SPECIES_EXTINCT_ABUNDANCE_THRESHOLD, max1=np.inf, min2=SPECIES_EXTINCT_ABUNDANCE_THRESHOLD, max2=np.inf):
    s1 = theta_star(x, min=min1, max=max1)
    s2 = theta_star(x, min=min2, max=max2)
    return np.outer(s1, s2)

def rank_abundance_distribution(x):
    return np.sort(x)

def survivors_rank_abundance_distribution(x, min=SPECIES_EXTINCT_ABUNDANCE_THRESHOLD):
    rad = rank_abundance_distribution(x)
    return rad[rad > min]

def abundance_distribution(x, **kwargs):
    return np.histogram(x, **kwargs)


#==============================================================================================================
#==============================================================================================================
#==============================================================================================================
'''
def classify_stability(dynamics, interaction_matrices, max_abundance=1e5, runs_max_difference=1e-5, **kwargs):
    N = len(interaction_matrices[0])
    runs = len(interaction_matrices)

    alpha = interaction_matrices[0]
    diverging_abundace = 0.0
    linearly_unstable = 0.0
    abundances = np.zeros((runs, N))
    n=0

    for r in range(runs):
        x0 = np.random.uniform(0, 1, N)
        t, x = dynamics(alpha, x0=x0, T_max=2000.0)
        abundances[r] = lv.x_star(x)

    for x in abundances:
        if np.any(x > max_abundance):
            diverging_abundace += 1

    for i in range(runs):
        for j in range(runs-1):
            n += 1
            if np.any(np.abs(abundances[i] - abundances[j]) > runs_max_difference):
                linearly_unstable += 1

    return diverging_abundace/runs, linearly_unstable/n
# '''
   

if __name__=="__main__":

    N = 100
    one = np.ones((N, N))

    mu = -1.0
    sigma = 1.0
    gamma = 0.0

    alpha = interaction_matrix(mu*one, sigma*one, gamma*one)
    t, x = run_dynamics(alpha, T_max=2000.0, print_progress=True)

