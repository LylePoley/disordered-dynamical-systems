from dash import Dash, Input, Output, State, html, dcc
import numpy as np
from src.components import ids, initial_values, constants
from utility.integrate import integrate
from .constants import BUFFER_SIZE, PLOT_WIDTH, REINTEGRATE_THRESHOLD, dt
from ..dynamical_systems import DisorderedDynamicalSystem

plot_updater = dcc.Interval(id=ids.plot_updater, interval=constants.REFRESH_RATE, n_intervals=0)

def render(app: Dash, dynamical_system: DisorderedDynamicalSystem) -> html.Div:
    """ dynamical_system(t, y, alpha) -> dy/dt"""

    @app.callback(
        Output(ids.t, 'data'),
        Output(ids.y, 'data'),
        Output(ids.t0_index, 'data'),
        Input(ids.t0_index, 'data'),
        State(ids.t, 'data'),
        State(ids.y, 'data'),
        State(ids.alpha, 'data')
    )
    def re_integrate_with_same_parameters(t0_index, t, y, alpha):
        if t[t0_index] == 0.0:
            t, y = integrate(dynamical_system, 
                            t0=0.0, 
                            number_of_timesteps=BUFFER_SIZE,
                            dt=dt, 
                            y0=initial_values.y0, 
                            args=(alpha,))

            t0_index = 0


        if t0_index + PLOT_WIDTH + REINTEGRATE_THRESHOLD >= BUFFER_SIZE:
            t = np.asarray(t, dtype=float)
            y = np.asarray(y, dtype=float)

            sol_t, sol_y = integrate(dynamical_system, 
                                    t0=t[-1], 
                                    number_of_timesteps=t0_index, 
                                    dt=dt, 
                                    y0=y[:, -1], 
                                    args=(alpha,))

            # copy the last t0_index elements of t and y to the beginning of the buffer
            t[:-t0_index] = t[t0_index:]
            y[:, :-t0_index] = y[:, t0_index:]

            # replace the rest with the new solution
            t[-t0_index:] = sol_t
            y[:, -t0_index:] = sol_y

            t0_index = 0


        return t, y, t0_index

    @app.callback(
        Output(ids.t, 'data', allow_duplicate=True),
        Output(ids.y, 'data', allow_duplicate=True),
        Output(ids.t0_index, 'data', allow_duplicate=True),
        Input(ids.alpha, 'data'),
        State(ids.t, 'data'),
        State(ids.y, 'data'),
        State(ids.t0_index, 'data'),
        prevent_initial_call=True
    )
    def re_integrate_with_new_parameters(alpha, t, y, t0_index):
        t = np.asarray(t, dtype=float)
        y = np.asarray(y, dtype=float)
        
        sol_t, sol_y = integrate(dynamical_system,
                                t0=t[t0_index + PLOT_WIDTH],
                                number_of_timesteps=BUFFER_SIZE - PLOT_WIDTH,
                                dt=dt,
                                y0=y[:, t0_index + PLOT_WIDTH],
                                args=(alpha,))
            
        # copy the last t0_index elements of t and y to the beginning of the buffer
        # and replace the rest with the new solution
        t[:PLOT_WIDTH] = t[t0_index:t0_index + PLOT_WIDTH]
        t[PLOT_WIDTH:] = sol_t

        y[:, :PLOT_WIDTH] = y[:, t0_index:t0_index + PLOT_WIDTH]
        y[:, PLOT_WIDTH:] = sol_y

        t0_index = 0

        return t, y, t0_index

    
    return html.Div([plot_updater])
