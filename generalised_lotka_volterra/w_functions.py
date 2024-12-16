from scipy.special import erfinv, erf, hermitenorm
import numpy as np


def wm1(x):
    return np.exp(-1/2*x**2)/np.sqrt(2*np.pi)
def w0(x):
    return 1/2*(1 + erf(x/np.sqrt(2)))

def w1(x):
    return wm1(x) + np.multiply(x, w0(x), where=(x != -np.inf), out=np.zeros_like(x))
def w2(x):
    return w0(x) + np.multiply(x, w1(x), where=(x != -np.inf), out=np.zeros_like(x))
def wm2(x):
    return np.multiply(-x, wm1(x), where=(x != np.inf), out=np.zeros_like(x))

def p_asymptotic(x):
    return (945/x**11 - 105/x**9 + 15/x**7 - 3/x**5 + 1/x**3 - 1/x)
def w0_x_minfty(x):
    return p_asymptotic(x)*wm1(x)
def w1_x_minfty(x):
    return wm1(x) + x*w0_x_minfty(x)
def w2_x_minfty(x):
    return w0_x_minfty(x) + x*w1_x_minfty(x)

def w2_over_w0(x, low=-5.5, high=-5.0):
    return np.piecewise(x, [x==-np.inf, np.logical_and(x > high, np.isfinite(x)), np.logical_and(x < low, np.isfinite(x))],
            [lambda x: 0.0,
            lambda x: w2(x)/w0(x), 
            lambda x: w2_x_minfty(x)/w0_x_minfty(x),
            lambda x: ((low - x)*w2(x)/w0(x) + (x - high)*w2_x_minfty(x)/w0_x_minfty(x))/(low - high)
        ])

def w1_over_w0(x, low=-5.5, high=-5.0):
    return np.piecewise(x, [x==-np.inf, np.logical_and(x > high, np.isfinite(x)), np.logical_and(x < low, np.isfinite(x))],
            [lambda x: 0.0,
            lambda x: w1(x)/w0(x), 
            lambda x: w1_x_minfty(x)/w0_x_minfty(x),
            lambda x: ((low - x)*w1(x)/w0(x) + (x - high)*w1_x_minfty(x)/w0_x_minfty(x))/(low - high)
        ])

def w0w2_over_w1_squared(x, low=-5.5, high=-5.0):
    return np.piecewise(x, [x==np.inf, x==-np.inf, np.logical_and(x > high, np.isfinite(x)), np.logical_and(x < low, np.isfinite(x))],
            [lambda x: 1.0,
            lambda x: 2.0,
            lambda x: w0(x)*w2(x)/w1(x)**2, 
            lambda x: w0_x_minfty(x)*w2_x_minfty(x)/w1_x_minfty(x)**2,
            lambda x: ((low - x)*w0(x)*w2(x)/w1(x)**2 + (x - high)*w0_x_minfty(x)*w2_x_minfty(x)/w1_x_minfty(x)**2)/(low - high)
        ])

def w0_inv(x):
    return np.sqrt(2)*erfinv(2*x - 1)

def w(n, x):
    '''
        All w_k(x) functions, defined by w_k'(x) = kw_{k-1}(x) for k positive and by 
        w_{-k}(x) = d^k/dx^k w_0(x) for negative k
    '''
    if not isinstance(n, int):
        raise ValueError("n must be an integer")

    if n >= 0:
        if n == 0:
            return w0(x)
        elif n == 1:
            return w1(x)
        else:
            return x*w(n-1, x) + (n-1)*w(n-2, x)
    else:
        return (-1)**(-(1 + n))*wm1(x)*hermitenorm(-(1 + n))(x)
    

