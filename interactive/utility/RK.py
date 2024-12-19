'''
Copied code from the Runge Kutta methods provided by scipy
'''
import numpy as np
from scipy.integrate import RK45
from scipy.integrate._ivp.common import (select_initial_step, validate_first_step)
import numba as nb
from jsonpickle import encode, decode
from functools import partial


@nb.njit
def norm(x):
    """Compute RMS norm."""
    return np.linalg.norm(x) / x.size ** 0.5


def initialize_state(fun, t0, y0, t_bound, max_step, rtol, atol, first_step, A, B, C, E, n_stages, error_estimator_order):
    direction = np.sign(t_bound - t0) if t_bound != t0 else 1
    f = fun(t0, y0)
    if first_step is None:
        h_abs = select_initial_step(fun, t0, y0, t_bound, max_step, f, direction, error_estimator_order, rtol, atol)
    else:
        h_abs = validate_first_step(first_step, t0, t_bound)
        
    state = {
        't': t0,
        'y': y0,
        't_old': None,
        'n': y0.size,
        'status': 'running',
        'direction': direction,
        't_bound': t_bound,
        'max_step': max_step,
        'rtol': rtol,
        'atol': atol,
        'f': f,
        'h_abs': h_abs,
        'K': np.empty((n_stages + 1, y0.size), dtype=y0.dtype),
        'error_exponent': -1 / (error_estimator_order + 1),
        'A': A,
        'B': B,
        'C': C,
        'E': E
    }
    
    return state

def RK45_state(fun, t0, y0, t_bound, rtol, atol, max_step=np.inf, first_step=None):
    order = 5
    error_estimator_order = 4
    n_stages = 6
    C = np.array([0, 1/5, 3/10, 4/5, 8/9, 1])
    A = np.array([
        [0, 0, 0, 0, 0],
        [1/5, 0, 0, 0, 0],
        [3/40, 9/40, 0, 0, 0],
        [44/45, -56/15, 32/9, 0, 0],
        [19372/6561, -25360/2187, 64448/6561, -212/729, 0],
        [9017/3168, -355/33, 46732/5247, 49/176, -5103/18656]
    ])
    B = np.array([35/384, 0, 500/1113, 125/192, -2187/6784, 11/84])
    E = np.array([-71/57600, 0, 71/16695, -71/1920, 17253/339200, -22/525,
                  1/40])

    return initialize_state(fun, t0, y0, t_bound, max_step, rtol, atol, 
                            first_step, n_stages=n_stages, 
                            error_estimator_order=error_estimator_order,
                            C=C, A=A, B=B, E=E)

def step(fun, state):
    SAFETY = 0.9
    MIN_FACTOR = 0.2
    MAX_FACTOR = 10

    if state['status'] != 'running':
        raise RuntimeError("Attempt to step on a failed or finished solver.")

    if state['n'] == 0 or state['t'] == state['t_bound']:
        state['t_old'] = state['t']
        state['t'] = state['t_bound']
        state['status'] = 'finished'
        return None

    min_step = 10 * np.abs(np.nextafter(state['t'], state['direction'] * np.inf) - state['t'])
    state['h_abs'] = min(state['max_step'], max(state['h_abs'], min_step))

    step_accepted = False
    step_rejected = False

    while not step_accepted:
        if state['h_abs'] < min_step:
            state['status'] = 'failed'
            return "Required step size is less than spacing between numbers."

        h = state['h_abs'] * state['direction']
        t_new = state['t'] + h

        if state['direction'] * (t_new - state['t_bound']) > 0:
            t_new = state['t_bound']

        h = t_new - state['t']
        state['h_abs'] = np.abs(h)

        y_new, f_new = rk_step(fun, state['t'], state['y'], state['f'], h, state['A'], state['B'], state['C'], state['K'])
        scale = state['atol'] + np.maximum(np.abs(state['y']), np.abs(y_new)) * state['rtol']
        error_norm = norm(np.dot(state['K'].T, state['E']) * h / scale)

        if error_norm < 1:
            state['h_abs'] *= min(MAX_FACTOR, SAFETY * error_norm ** state['error_exponent'] if error_norm != 0 else MAX_FACTOR)
            if step_rejected:
                state['h_abs'] = min(1, state['h_abs'])
            step_accepted = True
        else:
            state['h_abs'] *= max(MIN_FACTOR, SAFETY * error_norm ** state['error_exponent'])
            step_rejected = True

    state['t_old'] = state['t']
    state['t'] = t_new
    state['y'] = y_new
    state['f'] = f_new

    return None

def rk_step(fun, t, y, f, h, A, B, C, K):
    """Perform a single Runge-Kutta step."""
    K[0] = f
    for s, (a, c) in enumerate(zip(A[1:], C[1:]), start=1):
        dy = np.dot(K[:s].T, a[:s]) * h
        K[s] = fun(t + c * h, y + dy)

    y_new = y + h * np.dot(K[:-1].T, B)
    f_new = fun(t + h, y_new)
    K[-1] = f_new

    return y_new, f_new

def glv(t, y, alpha):
    dydt = y * (1 - y + alpha @ y)
    return dydt


if __name__ == '__main__':
    import pickle as pkl
    import json

    N = 2
    alpha = np.array([[0, 1], [-1, 0]])
    y0 = np.array([0.4, 0.6])
    glv_bound = partial(glv, alpha=np.array([[0, 1], [-1, 0]]))

    solver = RK45(fun=glv_bound, t0=0, y0=y0, t_bound=10, rtol=1e-3, atol=1e-6)
    state = RK45_state(fun=glv_bound, t0=0, y0=y0, t_bound=10, rtol=1e-3, atol=1e-6)

    solver.step()
    step(glv_bound, state)
    print(state['y'], solver.y)
    solver.step()
    step(glv_bound, state)
    print(state['y'], solver.y)

    state2 = decode(encode(state))

    print(state2, state)

