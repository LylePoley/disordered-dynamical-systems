from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components import style, ids, initial_values

mu_store = dcc.Store(id=ids.mu, data=initial_values.mu)

mu_input = dcc.Input(id=ids.mu_input, type='number', value=initial_values.mu, style=style.SIDEBAR_SLIDER)
mu_button = dbc.Button('Update mu', id=ids.mu_button, color='primary', size='sm', style=style.SIDEBAR_BUTTON)


def render(app: Dash, div_style: str | None = None) -> html.Div:
    @app.callback(
        Output(ids.mu, 'data'),
        Input(ids.mu_button, 'n_clicks'),
        State(ids.mu_input, 'value'),
        prevent_initial_call=True
    )
    def update_mu(n_clicks, mu):
        return mu
    
    return html.Div([mu_input, mu_button, mu_store], style=div_style)
