from scipy.integrate import solve_ivp
import numpy as np

def integrate(function: callable, t0: float, number_of_timesteps: int, dt: float, y0: float, **kwargs) -> tuple[np.ndarray, np.ndarray]:
    """
    Calls scipys solve_ivp function to integrate function over a time span. Values which are set automatically are 
    atol = 1e-8, rtol = 1e-5, and t_eval is also computed automatically.

    Args:
        function (callable): The function to integrate.
        t_span (tuple[float, float]): The time span to integrate over.
        y0 (float): The initial value of the function.
        **kwargs: Additional keyword arguments to pass to the solve_ivp function.

    Returns:
        tuple[np.ndarray, np.ndarray]: The time points and the values of the function at those time points.
    """
    tf = t0 + number_of_timesteps * dt

    t_eval = np.linspace(t0, tf, number_of_timesteps)
    solution = solve_ivp(function, t_span=(t0, tf), y0=y0, 
                        atol=1e-8, rtol=1e-5, t_eval=t_eval, **kwargs)
    
    return solution.t, solution.y