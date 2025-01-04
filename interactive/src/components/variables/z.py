from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import numpy as np

from src.components import style, ids, initial_values

z_store = dcc.Store(id=ids.z, data=initial_values.z)

z_reset_button = dbc.Button('Reset z', id=ids.z_reset_button, color='primary', style=style.SIDEBAR_BUTTON)

def render(app: Dash, div_style: str | None = None) -> html.Div:
    @app.callback(
        Output(ids.z, 'data'),
        Input(ids.z_reset_button, 'n_clicks'),
        prevent_initial_call=True
    )
    def reset_z(n_clicks):
        return np.random.normal(0, 1, (initial_values.N, initial_values.N))

    
    return html.Div([z_reset_button, z_store], style=div_style)
