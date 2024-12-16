'''
    Convenience functions for integrating ODEs of the following form
    dx_i/dt = F(x_1, ..., x_N)

    where F is a function that takes in an array of length N and returns an array of length N
'''

from scipy.integrate import solve_ivp
from tqdm import tqdm
import numpy as np

_T_MAX = 1000.0
_STATIONARY_T_MAX = 10000.0

def _print_progress_wrapper(dynamical_system, progress_bar, state):
    '''
        Given a dynamical system, produces a wrapped system which uses a tqdm progress_bar to output its progress during integration.
        This function is used internally to display progress meters during integration.

        PARAMETERS:
        dynamical_system: function(t, X, *args) -> dX/dt
        progress_bar: tqdm progress bar
        state: [last_t, dt] where last_t is the last time step and dt is the time step size

        RETURNS:
        wrapped: function(t, X, *args) -> dX/dt
    '''
    def wrapped_system(t, X, *args):
        last_t, dt = state
        n = int((t - last_t)/dt)
        progress_bar.update(n)
        state[0] = last_t + dt * n

        return dynamical_system(t, X, *args)
    
    return wrapped_system

def run_until_stationary(dynamical_system, dynamical_system_args=None, *, stationary_tolerance=1e-5, x0=None, t_max=_STATIONARY_T_MAX, print_progress=False, rtol=1e-5, **solver_kwargs):
    '''
        Similar to "run", but integrates the system until it reaches a stationary point, or reaches the time limit t_max.

        PARAMETERS:
        All are as in "run", except for:
        stationary_tolerance: tolerance for the stationary point, the system is considered to be stationary if ||dX/dt|| < stationary_tolerance
        where ||.|| is the L2 norm, i.e. ||x|| = sqrt(x_1**2 + x_2**2 + ... + x_N**2)

        RETURNS:
        solution, t_stationary
        solution: as in "run"
        t_stationary: time at which the system reached a stationary point, or None if it did not reach a stationary point within the time limit
    '''

    if np.any(x0 == None):
        raise ValueError("Initial conditions must be specified")


    def event(t, y, *args):
        norm_dydt = np.sqrt(np.average(dynamical_system(t, y, *args)**2))

        # Check if the system has reached a stationary point
        if norm_dydt < stationary_tolerance: 
            return 0
        
        return norm_dydt

    # Ensure the event function stops integration when it returns 0
    event.terminal = True

    solution = run(dynamical_system, 
               dynamical_system_args=dynamical_system_args, 
               x0=x0, 
               t_max=t_max, 
               print_progress=print_progress, 
               rtol=rtol, 
               events=event, 
               **solver_kwargs)
    
    return solution, solution.t_events[0][-1] if len(solution.t_events[0]) > 0 else None

def run(dynamical_system, dynamical_system_args=None, *, x0=None, t_max=_T_MAX, print_progress=False, rtol=1e-5, **solver_kwargs):
    '''
        Given a dynamical system, integrates it over the time interval [0, T_max] with initial conditions x0.
        This function assumes that the dynamical system takes no additional arguments beyond time and state.

        PARAMETERS:
        dynamical_system: function(t, X) -> dX/dt
        dynamical_system_args: additional arguments to pass to the dynamical system
        x0: initial conditions
        T_max: maximum time
            Defaults to 1000.0
        print_progress: whether to display a progress bar
        rtol: relative tolerance for the solver
        kwargs: additional arguments to pass to the solver

        RETURNS:
        solution: solution object returned by scipy.integrate.solve_ivp
            solution.t: time steps
            solution.y: x(t), solution.y[i, t] = x_i(t)
            solution.success: whether the integration was successful
            solution.message: message from the solver   

        RAISES:
        ValueError: if initial conditions x0 are not provided 

        EXAMPLE:
        ...

    '''

    if np.any(x0 == None):
        raise ValueError("Initial conditions must be specified")

    if print_progress:
        with tqdm(total=100, unit="‰") as pbar:
            solution = solve_ivp(_print_progress_wrapper(dynamical_system, pbar, [0, t_max/100]),
                             t_span=(0, t_max), 
                             y0=x0, 
                             args=dynamical_system_args, 
                             rtol=rtol, 
                             vectorized=True, 
                             **solver_kwargs)
    else:
        solution = solve_ivp(dynamical_system, 
                        t_span=(0, t_max), 
                        y0=x0, 
                        args=dynamical_system_args, 
                        rtol=rtol, 
                        vectorized=True, 
                        **solver_kwargs)

    return solution

#==============================================================================================================
#==============================================================================================================
#==============================================================================================================

if __name__=="__main__":
    import matplotlib.pyplot as plt

    N = 1000
    interaction_matrix = np.random.normal(0, 0.5/np.sqrt(N), (N, N))

    def dynamical_system(t, X, interaction_matrix):
        return X*(1 - X + interaction_matrix @ X)
    
    solution, time = run_until_stationary(dynamical_system, dynamical_system_args=(interaction_matrix,), x0=np.random.uniform(0, 1, N), t_max=1000.0, print_progress=True, stationary_tolerance=0.5e-4)
    print(time)
    plt.plot(solution.t, solution.y.T)
    plt.show()

