from dash import Dash, Input, Output, State, html, dcc
import numpy as np

from src.components.registers import (ids, initial_values, types)

interaction_matrix_store = dcc.Store(
    id=ids.interaction_matrix, data=initial_values.interaction_matrix)


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.interaction_matrix, 'data'),
        Input(ids.interaction_mean, 'data'),
        Input(ids.interaction_standard_deviation, 'data'),
        Input(ids.interaction_noise, 'data'),
        State(ids.number_of_agents, 'data'),
        prevent_initial_call=True
    )
    def update_alpha(mean: float, standard_deviation: float, noise: types.Matrix, N: int) -> types.Matrix:
        return mean/N + standard_deviation*np.asarray(noise)/np.sqrt(N)

    return html.Div([interaction_matrix_store])
