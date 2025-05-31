from dash import Dash, Input, Output, State, html, dcc

import numpy as np

from constants import (ids, initial_values, types)

interaction_matrix_store = dcc.Store(
    id=ids.interaction_matrix, data=initial_values.interaction_matrix)


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.interaction_matrix, 'data'),
        Input(ids.interaction_noise, 'data'),
        State(ids.interaction_mean_input, 'value'),
        State(ids.interaction_standard_deviation_input, 'value'),
        prevent_initial_call=True
    )
    def update_alpha(noise: types.Matrix, mean: float, standard_deviation: float) -> types.Matrix:
        z = np.asarray(noise)
        N = z.shape[0]

        return mean/N + standard_deviation*z/np.sqrt(N)

    return html.Div([interaction_matrix_store])
