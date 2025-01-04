from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components import style, ids, initial_values

sigma_store = dcc.Store(id=ids.sigma, data=initial_values.sigma)

sigma_input = dcc.Input(id=ids.sigma_input, type='number', value=initial_values.sigma, style=style.SIDEBAR_SLIDER)
sigma_button = dbc.Button('Update sigma', id=ids.sigma_button, color='primary', size='sm', style=style.SIDEBAR_BUTTON)


def render(app: Dash, div_style: str | None = None) -> html.Div:
    @app.callback(
        Output(ids.sigma, 'data'),
        Input(ids.sigma_button, 'n_clicks'),
        State(ids.sigma_input, 'value'),
        prevent_initial_call=True
    )
    def update_sigma(n_clicks, sigma):
        return sigma
    
    return html.Div([sigma_input, sigma_button, sigma_store], style=div_style)
