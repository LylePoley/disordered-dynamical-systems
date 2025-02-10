from dash import Dash, Input, Output, State, html
import dash_bootstrap_components as dbc
import numpy as np
from src.components.registers import ids, types
from src.components import style
from utility.integrate import integrate, draw_initial_condition
from .registers.constants import dt
from src.components.variables.dynamical_system import id_to_dynamical_system

from src.components.registers.types import Vector, Matrix, OdeSolution


integrate_button = dbc.Button(
    'Integrate dynamics',
    id=ids.integrate_button,
    color='primary',
    size='sm',
    style=style.SIDEBAR_BUTTON
)


def render(app: Dash, style: dict[str, str] | None = None) -> html.Div:

    @app.callback(
        Output(ids.time, 'data'),
        Output(ids.y, 'data'),
        Input(ids.integrate_button, 'n_clicks'),
        State(ids.time_final_input, 'value'),
        State(ids.time, 'data'),
        State(ids.y, 'data'),
        State(ids.interaction_matrix, 'data'),
        State(ids.dynamical_system_dropdown, 'value'),
    )
    def integrate_dynamics(
        n_clicks: int,
        t_final: float,
        time: Vector,
        y: OdeSolution,
        interaction_matrix: Matrix,
        dynamical_system_id: int) \
            -> tuple[Vector, OdeSolution]:
        
        """ dynamical_system(t, y, alpha) -> dy/dt """
        dynamical_system = id_to_dynamical_system(dynamical_system_id)
        y = np.array(y)
        y0 = y[:, 0]
        
        if len(interaction_matrix) != len(y0):
            N = len(interaction_matrix)
            y0 = draw_initial_condition(N)

        # TODO this should only integrate if necessary
        # TODO set max possible array sizes
        t_new, y_new = integrate(dynamical_system,
                                 integration_range=(0.0, t_final),
                                 dt=dt,
                                 y0=y0,
                                 args=(interaction_matrix,))

        return t_new, y_new

    return html.Div([integrate_button], style=style)
