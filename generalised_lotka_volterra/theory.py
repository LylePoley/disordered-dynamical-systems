import numpy as np
from scipy.optimize import root
from scipy.sparse.linalg import eigs
from functools import partial
from generalised_lotka_volterra.w_functions import *
import generalised_lotka_volterra.simulation as sim
from scipy.interpolate import interpn

#==============================================================================================================
#================================================= ELLIPTICAL THEORY ==========================================
#==============================================================================================================

def _delta(sigma, gamma, delta_guess=0.1):
    return root(lambda d : sigma**2 - w2(d)/(w2(d) + gamma*w0(d))**2, [delta_guess]).x[0]

class elliptical_theory:
    '''
    This class contains the solutions to the fixed point equations for non-finely structured, fully connected, generalised Lotka-Volterra equations.
    '''
    def __init__(self, mu=0.0, sigma=1.0, gamma=0.0):
        self.mu = mu
        self.sigma = sigma
        self.gamma = gamma

        self.Delta = None


    def solve_fixed_point_equations(self, *, delta_guess=0.1):
        '''
            Must call this function first to get meaningful results from the other functions
        '''
        self.Delta = _delta(self.sigma, self.gamma, delta_guess)  


    def all_order_parameters(self):
        '''
            returns all order parameters in the order 
            phi, M, q, chi, chi_T, chi_2
        '''
        chi = self.chi()
        phi = self.phi()
        M = self.M()
        q = self.q()
        chi_T = self.chi_T()
        chi_2 = self.chi_2()

        return phi, M, q, chi, chi_T, chi_2   

    def chi(self):
        return w0(self.Delta) + self.gamma*w0(self.Delta)**2 / w2(self.Delta)
    def phi(self):
        return w0(self.Delta)
    def M(self):
        return (self.Delta * w2(self.Delta) / w1(self.Delta) / (w2(self.Delta) + self.gamma*w0(self.Delta)) - self.mu)**(-1)
    def q(self):
        return (self.M() * w2(self.Delta) / self.sigma / w1(self.Delta) / (w2(self.Delta) + self.gamma*w0(self.Delta)))**2
    def chi_T(self):
        return (w1(self.Delta) - self.Delta*w0(self.Delta)) / self.sigma / np.sqrt(self.q())
    def chi_2(self):
        return -self.Delta*(w1(self.Delta) - self.Delta*w0(self.Delta)) / self.sigma**2 / self.q()

    def rank_abundance_distribution(self, alpha):
        M = self.M()
        q = self.q()
        chi = self.chi()

        m = (1 + self.mu*M)/(1 - self.gamma*self.sigma**2*chi)
        Sigma = self.sigma*np.sqrt(q)/(1 - self.gamma*self.sigma**2*chi)

        val = m - Sigma * w0_inv(1 - alpha)
        return np.heaviside(val, 0)*np.abs(val)
    
    def abundance_distribution(self, x):
        phi = self.phi()
        M = self.M()
        q = self.q()
        chi = self.chi()

        m = (1 + self.mu*M)/(1 - self.gamma*self.sigma**2*chi)
        Sigma = self.sigma*np.sqrt(q)/(1 - self.gamma*self.sigma**2*chi)

        return 1/np.sqrt(2*np.pi*Sigma**2)*np.exp(-(x-m)**2/Sigma**2/2)
    
    @staticmethod
    def linear_instability(*, sigma=None, gamma=None):
        '''
            given sigma, returns the value of gamma at which the system becomes linearly unstable.
            Vice versa if gamma is given. The condition for linear instability is 
            sigma**2 = 2/(1 + gamma)**2
            returns sigma, gamma
        '''
        if sigma==None and gamma==None:
            raise ValueError("Either sigma or gamma must be given")
        elif sigma==None:
            sigma = np.sqrt(2)/(1 + gamma)
        elif gamma==None:
            gamma = np.sqrt(2)/sigma - 1

        return sigma, gamma
        
    @staticmethod
    def M_to_infinity_conditions(*, mu=None, sigma=None, gamma=None, Delta=None):
        '''
            Given any two of mu, sigma, and gamma, returns the value of the third at which M becomes infinite

            returns mu, sigma, gamma
        '''
        cond_1 = sigma**2 - w2(Delta)/(w2(Delta) + gamma*w0(Delta))**2
        cond_2 = mu - Delta * w2(Delta) / w1(Delta) / (w2(Delta) + gamma*w0(Delta))

        return np.r_[cond_1, cond_2]
        

#==============================================================================================================
#============================================ FINELY STRUCTURED THEORY ========================================
#==============================================================================================================

def stationary_fixed_point_equations(Mqchi, u_mat, s_mat, t_mat, N):
    '''
    vector of all 3N fixed point equations in format condition_M, condition_q, condition_chi
    '''
    M, q, chi = np.split(Mqchi, 3)
    
    uM = u_mat@M/N
    sq = s_mat@q/N
    tchi = t_mat@chi/N

    Delta = np.piecewise(sq, [sq > 0, 1 + uM == 0], [lambda x: (1 + uM)/np.sqrt(x), lambda x: 0.0, lambda x: np.sign(1 + uM)*np.inf])

    condition_M = M - np.multiply(np.sqrt(sq), w1(Delta)/(1 - tchi), where=(sq > 0), out=np.zeros_like(M))
    condition_q = q - np.multiply(sq, w2(Delta)/(1 - tchi)**2, where=(sq > 0), out=np.zeros_like(q))
    condition_chi = chi - w0(Delta)/(1 - tchi)

    return np.r_[condition_M, condition_q, condition_chi]

def diverging_abundance_equations(Mqchi, u_mat, s_mat, t_mat, N, epsilon=0.0):
    '''
    vector of all 3N fixed point equations in format conditionM, condition_q, condition_chi
    '''
    M, q, chi = np.split(Mqchi, 3)

    uM = u_mat@M/N
    sq = s_mat@q/N
    tchi = t_mat@chi/N
    
    Delta = np.piecewise(sq, [sq > 0, 1 + uM == 0], [lambda x: (epsilon + uM)/np.sqrt(x), lambda x: 0.0, lambda x: np.sign(epsilon + uM)*np.inf])

    condition_M = M - np.multiply(np.sqrt(sq), w1(Delta)/(1 - tchi), where=(sq != 0), out=np.zeros_like(M))
    condition_q = q - np.multiply(sq, w2(Delta)/(1 - tchi)**2, where=(sq != 0), out=np.zeros_like(q))
    condition_chi = chi - w0(Delta)/(1 - tchi)
    condition_q_normalised = np.average(q) - 1

    return np.r_[condition_M, condition_q, condition_chi, condition_q_normalised]

def linear_instability_equations(Mqchi, u_mat, s_mat, t_mat, N):
    M, q, chi = np.split(Mqchi, 3)

    uM = u_mat@M/N
    sq = s_mat@q/N
    tchi = t_mat@chi/N
    
    Delta = np.piecewise(sq, [sq > 0, 1 + uM == 0], [lambda x: (1 + uM)/np.sqrt(x), lambda x: 0.0, lambda x: np.sign(1 + uM)*np.inf])

    condition_M = M - np.multiply(np.sqrt(sq), w1(Delta)/(1 - tchi), where=(sq != 0), out=np.zeros_like(M))
    condition_q = q - np.multiply(sq, w2(Delta)/(1 - tchi)**2, where=(sq != 0), out=np.zeros_like(q))
    condition_chi = chi - w0(Delta)/(1 - tchi)
    condition_linear_instability = eigs(chi/(1 - tchi)*s_mat/N, k=1, which='LR', return_eigenvectors=False)[0].real - 1

    return np.r_[condition_M, condition_q, condition_chi, condition_linear_instability]

#==============================================================================================================
#================================== SOLVING FIXED POINT EQUATIONS =============================================
#==============================================================================================================
    
def _find_fixed_point_from_guess(u_mat, s_mat, t_mat, Mqchi_guess):
    '''
    This function attempts to find the point at which each of the fixed point conditions in fs_glv_fixed_point_equations are equal to 0.
    '''
    N = len(u_mat)

    fixed_point_conditions = partial(
        stationary_fixed_point_equations, u_mat=u_mat, s_mat=s_mat, t_mat=t_mat, N=N)
    

    return root(fixed_point_conditions, Mqchi_guess).x


def _interpolate_array2d(A, N_new):
    N = A.shape[0]
    x = np.linspace(0, 1, N)
    y = np.linspace(0, 1, N)

    x_new = np.linspace(0, 1, N_new)
    y_new = np.linspace(0, 1, N_new)

    X, Y = np.meshgrid(x_new, y_new)

    return interpn((x, y), A, np.array([X, Y]).T)

def _find_fixed_point(u_mat, s_mat, t_mat, *, N0=25, N_more=None, N_final=None, iterations0=50, print_progress=False):
    '''
        This function attempts to find the fixed point of the generalised Lotka-Volterra 
        equations by first solving for the fixed point of a smaller system of size N0 and 
        then using this as the initial conditions for a larger system of size N1 > N0. 
        There is also the option of ramping up from N0 to N_final with progressively larger 
        system sizes in N_more
    '''
    if N_final==None:
        N_final = u_mat.shape[0]
    if N_more==None:
        N_more = np.array([N_final])
    else:
        N_more = np.r_[N_more, N_final] 

    phi0 = np.zeros(N0)
    M0 = np.zeros(N0)
    q0 = np.zeros(N0)

    # linearly interpolate statistics to smaller matrix size
    u0 = _interpolate_array2d(u_mat, N0)
    s0 = _interpolate_array2d(s_mat, N0)
    t0 = _interpolate_array2d(t_mat, N0)

    sigma0 = np.sqrt(s0)
    gamma0 = t0/np.sqrt(s0*s0.T)

    interaction_matrices0 = sim.interaction_matrices(u0, sigma0, gamma0, iterations0)

    # find initial guess by integrating low dimensional equations with same statistics as the full system
    x0 = sim.iterate_dynamics(interaction_matrices0, print_progress=print_progress)

    phi0 = sim.phii(x0)
    M0 = sim.Mi(x0)
    q0 = sim.qi(x0)

    Delta0 = w0_inv(phi0)

    # derived from the fixed point equations, computing chi from the simulated value of phi
    chi0 = np.divide(M0**2*w0w2_over_w1_squared(Delta0), q0, where=q0!=0, out=np.zeros_like(M0))

    if print_progress:
        print(f"Solving system of size {N0=}")

    Mqchi = _find_fixed_point_from_guess(u0, s0, t0, np.r_[M0, q0, chi0])
    M, q, chi = np.split(Mqchi, 3)

    if np.any(N_more!=None):
        for i, N in enumerate(N_more):
            idx_prev = np.linspace(0, 1, len(M))
            idx = np.linspace(0, 1, N)

            # linearly interpolate the solution up to the larger system size
            M = np.interp(idx, idx_prev, M)
            q = np.interp(idx, idx_prev, q)
            chi = np.interp(idx, idx_prev, chi)

            u = _interpolate_array2d(u_mat, len(M))
            s = _interpolate_array2d(s_mat, len(M))
            t = _interpolate_array2d(t_mat, len(M))

            if print_progress:
                print(f"Solving system of size {N=}")

            Mqchi = _find_fixed_point_from_guess(u, s, t, np.r_[M, q, chi])
            M, q, chi = np.split(Mqchi, 3)
    
    if N_final < len(u_mat):
        idx_prev = np.linspace(0, 1, len(M))
        idx = np.linspace(0, 1, len(u_mat))

        M = np.interp(idx, idx_prev, M)
        q = np.interp(idx, idx_prev, q)
        chi = np.interp(idx, idx_prev, chi)

    return np.r_[M, q, chi]

#==============================================================================================================
#===================================== THEORY WRAPPED IN A CLASS ==============================================
#==============================================================================================================
    

class theory:
    '''
    Collection of expressions for order parameters in the finely structured Lotka Volterra 
    model in terms of other parameters. All expressions are ultimately derived from the 
    fixed point equations.

        chi_i u_i = phi_i
        M_i u_i = w1(Delta_i) sqrt(sum_j s_{ij}q_j/N)
        q_i u_i^2 = w2(Delta_i) sum_j s_{ij}q_j/N

        Delta_i sqrt(sum_j s_{ij}q_j/N) = 1 + sum_j u_{ij}M_j/N
        u_i = 1 - sum_jt_{ij}chi_j/N
    '''

    def __init__(self, mu_mat, sigma_mat, gamma_mat, sigma_min=1e-8):
        self.N = len(mu_mat)

        # values of sigma which are too small cause numerical instability
        sigma_mat_nonzero = np.where(sigma_mat > sigma_min, sigma_mat, sigma_mat + sigma_min)

        self.u_mat = mu_mat
        self.s_mat = sigma_mat_nonzero**2
        self.t_mat = gamma_mat*sigma_mat_nonzero*sigma_mat_nonzero.T

        self.m_Mi = np.zeros(self.N)
        self.m_qi = np.zeros(self.N)
        self.m_chii = np.zeros(self.N)

    def solve_fixed_point_equations(self, *, N0=25, N_final=None, print_progress=False, iterations=50, N_more=None, Mqchi_guess=None):
        if self.N < N0:
            N0 = self.N
        if np.any(Mqchi_guess==None):
            Mqchi = _find_fixed_point(self.u_mat, self.s_mat, self.t_mat, N0=N0, print_progress=print_progress, iterations0=iterations, N_more=N_more, N_final=N_final)
        else:

            Mqchi = _find_fixed_point_from_guess(self.u_mat, self.s_mat, self.t_mat, Mqchi_guess)

        self.m_Mi, self.m_qi, self.m_chii = np.split(Mqchi, 3)
        return Mqchi


    def phii(self):
        return self.m_chii*(1 - self.t_mat@self.m_chii/self.N)
    def Mi(self):
        return self.m_Mi
    def qi(self):
        return self.m_qi
    def chii(self):
        return self.m_chii
    def chi_Ti(self):
        return np.divide(wm1(self.Deltai()), np.sqrt(self.s_mat@self.qi()/self.N), where=self.s_mat@self.qi()==0, out=np.zeros_like(self.Mi()))
    def chi_2i(self):
        return np.divide(wm2(self.Deltai()), (self.s_mat@self.qi()/self.N), where=self.s_mat@self.qi()==0, out=np.zeros_like(self.Mi()))
    def Deltai(self):
        return w0_inv(self.phii())

    def phi(self):
        return np.average(self.phii())
    def M(self):
        return np.average(self.Mi())
    def q(self):
        return np.average(self.qi())
    def chi(self):
        return np.average(self.chii())
    def chi_T(self):
        return np.average(self.chi_Ti())
    def chi_2(self):
        return np.average(self.chi_2i())
    
    def abundance_distribution(self, x):

        mean = (1 + self.u_mat@self.Mi/self.N)/(1 - self.t_mat@self.chii/self.N)
        variance = self.s_mat@self.qi/self.N/((1 - self.t_mat@self.chii/self.N))**2

        try:
            return np.average(np.exp(-1/2*(x[:, np.newaxis] - mean)**2/variance)/np.sqrt(2*np.pi*variance), axis=1)
        except:
            return np.average(np.exp(-1/2*(x - mean)**2/variance)/np.sqrt(2*np.pi*variance))
    

#==============================================================================================================
#==============================================================================================================
#==============================================================================================================



if __name__=='__main__':
    import matplotlib.pyplot as plt
    # import generalised_lotka_volterra_V3 as glv
    import finely_structured_random_matrix as fs
    import utility as utility
    import numba as nb
    import numpy as np

    N = 500

    mu = utility.function_to_array2d(N, nb.njit(lambda i, j : 50 if i < j else -50))
    sigma = np.full((N, N), 1.0)
    gamma = np.full((N, N), 0.0)


    S = fs.fs_statistics(mu, sigma, gamma)
    th = theory(*S)
    th.solve_fixed_point_equations(print_progress=True, N_more=[50])

    alphas = [fs.fsrm_instance(*S) for _ in range(20)]

    x_star_mat = sim.iterate_dynamics(alphas, print_progress=True)

    fig, ax = plt.subplots(1, 3, figsize=(18, 5))
    ax[0].plot(sim.Mi(x_star_mat))
    ax[0].plot(th.Mi())

    ax[1].plot(sim.phii(x_star_mat))
    ax[1].plot(th.phii())

    ax[2].plot(sim.qi(x_star_mat))
    ax[2].plot(th.qi())

    print(sim.Mi(x_star_mat))
    plt.show()
    