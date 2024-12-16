'''
    This file contains classes and functions for working with finely structured random matrices.

    To define your own finely structured random matrix model using this code you need three matrices

    mu(i, j), sigma(i, j), gamma(i, j)

    These matrices must each be N x N
'''

import numpy as np
import numba as nb

@nb.njit
def fsrm_instance(mu_mat, sigma_mat, gamma_mat):
    '''
    does the same as finely_structured_random_matrix, but takes in matrices instead of functions
    '''
    N = len(mu_mat)
    result = np.full((N, N), 0.0)

    for i in range(N):
        for j in range(i):

            g = gamma_mat[i, j]

            z1 = np.random.normal(0, 1)/np.sqrt(N)
            z2 = np.random.normal(0, 1)/np.sqrt(N)

            result[i, j] = sigma_mat[i, j]*z1
            result[j, i] = sigma_mat[j, i]*(g*z1 + np.sqrt(1 - g**2)*z2)  

            a = result[i, j]
            b = result[j, i] 

    result += mu_mat/N

    return result

@nb.njit 
def elliptical_instance(N, mu, sigma, gamma):
    '''
    does the same as finely_structured_random_matrix, but takes in numbers instead of functions
    '''
    result = np.full((N, N), 0.0)

    for i in range(N):
        for j in range(i):

            g = gamma

            z1 = np.random.normal(0, 1)/np.sqrt(N)
            z2 = np.random.normal(0, 1)/np.sqrt(N)

            result[i, j] = sigma*z1
            result[j, i] = sigma*(g*z1 + np.sqrt(1 - g**2)*z2)   

    result += mu/N

    return result

def ust_to_mu_sigma_gamma(u, s, t):
    mu = u
    sigma = np.sqrt(s)
    gamma = np.divide(t, np.sqrt(s*s.T), where=s*s.T>0, out=np.zeros_like(t))

    return mu, sigma, gamma

def mu_sigma_gamma_to_ust(mu, sigma, gamma):
    u = mu
    s = sigma**2
    t = gamma*sigma*sigma.T

    return u, s, t


class elliptical_spectrum:
    def __init__(self, mu, sigma, gamma):
        self.mu = mu
        self.sigma = sigma
        self.gamma = gamma

    def bulk_boundary(self, no_of_points=250):
        phi = np.linspace(0, 2*np.pi, no_of_points)
        
        return self.sigma*(np.exp(-1j*phi) + self.gamma*np.exp(1j*phi))
    
    def outlier(self):
        return self.mu + self.gamma*self.sigma**2/self.mu
    
    def bulk_edge(self):
        return self.sigma*(1 + self.gamma)
    
    def max_eigenvalue(self):
        if self.mu**2 > self.sigma:
            return self.outlier()
        else:
            return self.bulk_edge()



class fs_statistics:
    @classmethod
    def from_ust(cls, u_mat, s_mat, t_mat):
        assert u_mat.shape == s_mat.shape == t_mat.shape

        mu_mat, sigma_mat, gamma_mat = ust_to_mu_sigma_gamma(u_mat, s_mat, t_mat)
        cls(mu_mat, sigma_mat, gamma_mat)
        
    def __init__(self, mu_mat, sigma_mat, gamma_mat):
        assert mu_mat.shape == sigma_mat.shape == gamma_mat.shape

        self.mu_mat = mu_mat
        self.sigma_mat = sigma_mat
        # deals with floating point errors which give gamma > 1 or gamma < -1
        self.gamma_mat = np.where(np.abs(gamma_mat) < 1, gamma_mat, np.sign(gamma_mat))

    def __iter__(self):
        yield self.mu_mat
        yield self.sigma_mat
        yield self.gamma_mat

    def u(self):
        return self.mu_mat
    def s(self):
        return self.sigma_mat**2
    def t(self):
        return self.gamma_mat*self.sigma_mat*self.sigma_mat.T
    

