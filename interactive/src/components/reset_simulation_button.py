from dash import Dash, Input, Output, html
import dash_bootstrap_components as dbc
from .constants import BUFFER_SIZE
import numpy as np

from src.components import style, ids, initial_values

reset_simulation_button = dbc.Button('Reset simulation', id=ids.reset_simulation_button, color='primary', style=style.SIDEBAR_BUTTON)


def render(app: Dash, div_style: str | None = None) -> html.Div:
    @app.callback(
        Output(ids.t, 'data', allow_duplicate=True),
        Output(ids.y, 'data', allow_duplicate=True),
        Output(ids.t0_index, 'data', allow_duplicate=True),
        Input(ids.reset_simulation_button, 'n_clicks'),
        prevent_initial_call=True
    )
    def reset_simulation(n_clicks):
        t = np.zeros(BUFFER_SIZE)
        y = np.zeros((initial_values.N, BUFFER_SIZE))
        t[0] = 0.0
        y[:, 0] = initial_values.y0
        t0_index = 0
        return t, y, t0_index

    
    return html.Div([reset_simulation_button], style=div_style)
