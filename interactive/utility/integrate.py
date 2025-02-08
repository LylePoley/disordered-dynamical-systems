from scipy.integrate import solve_ivp
import numpy as np
from typing import Callable

def integrate(function: Callable, integration_range: tuple[float, float], dt: float, y0: float, **kwargs) -> tuple[np.ndarray, np.ndarray]:
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

    solution = solve_ivp(function, t_span=integration_range, y0=y0, 
                        atol=1e-8, rtol=1e-5, **kwargs)
    
    return solution.t, solution.y