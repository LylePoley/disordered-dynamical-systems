from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import numpy as np
from constants import ids
from utility.integrate import integrate, draw_initial_condition
from components.variables.dynamical_system import id_to_dynamical_system

from constants.types import Vector, Matrix, OdeSolution


integrate_button = dbc.Button(
    'Integrate dynamics',
    id=ids.integrate_button,
    color="secondary",
    class_name="sidebar-button"
)

integrate_tooltip = dbc.Tooltip(
    [
        dcc.Markdown(
            r"""Integrates the dynamics in the range $0<t<T$. Note that the
            plot will not change if none of the interaction matrix, initial
            condition, or dynamical system are changed.""",
            mathjax=True)],
    target=ids.integrate_button
)

def render(app: Dash, class_name: str | None = None) -> html.Div:

    @app.callback(
        Output(ids.time, 'data'),
        Output(ids.y, 'data'),
        Input(ids.integrate_button, 'n_clicks'),
        State(ids.time_final_input, 'value'),
        State(ids.time, 'data'),
        State(ids.y, 'data'),
        State(ids.initial_condition, 'data'),
        State(ids.interaction_matrix, 'data'),
        State(ids.dynamical_system_dropdown, 'value'),
    )
    def integrate_dynamics(
        n_clicks: int,
        t_final: float,
        time: Vector,
        y: OdeSolution,
        initial_condition: Vector,
        interaction_matrix: Matrix,
        dynamical_system_id: int) \
            -> tuple[Vector, OdeSolution]:

        """ dynamical_system(t, y, alpha) -> dy/dt """
        dynamical_system = id_to_dynamical_system(dynamical_system_id)
        y = np.array(y)
        y0 = np.array(initial_condition)

        if len(interaction_matrix) != len(y0):
            N = len(interaction_matrix)
            y0 = draw_initial_condition(N)

        # TODO this should only integrate if necessary
        # TODO set max possible array sizes
        t_new, y_new = integrate(dynamical_system,
                                 integration_range=(0.0, t_final),
                                 y0=y0,
                                 args=(interaction_matrix,))

        return t_new, y_new

    return html.Div([integrate_button, integrate_tooltip], className=class_name)
