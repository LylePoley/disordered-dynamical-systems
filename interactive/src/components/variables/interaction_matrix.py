from dash import Dash, Input, Output, State, html, dcc
import numpy as np

from src.components.registers import (ids, initial_values, types)

interaction_matrix_store = dcc.Store(
    id=ids.interaction_matrix, data=initial_values.interaction_matrix)


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.interaction_matrix, 'data'),
        Input(ids.interaction_mean_input, 'value'),
        Input(ids.interaction_standard_deviation_input, 'value'),
        Input(ids.interaction_noise, 'data'),
        prevent_initial_call=True
    )
    def update_alpha(mean: float, standard_deviation: float, noise: types.Matrix) -> types.Matrix:
        z = np.asarray(noise)
        N = z.shape[0]

        return mean/N + standard_deviation*z/np.sqrt(N)

    return html.Div([interaction_matrix_store])
