from dash import Dash, Input, Output, html, dcc
import numpy as np

from src.components import ids, initial_values

alpha_store = dcc.Store(id=ids.alpha, data=initial_values.alpha)

def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.alpha, 'data'),
        Input(ids.mu, 'data'),
        Input(ids.sigma, 'data'),
        Input(ids.z, 'data'),
        prevent_initial_call=True
    )
    def update_alpha(mu, sigma, z):
        return mu/initial_values.N + sigma*np.asarray(z)/np.sqrt(initial_values.N)

    return html.Div([alpha_store])
