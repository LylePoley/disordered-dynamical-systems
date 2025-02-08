from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components.registers import ids, initial_values
from src.components import style

number_of_agents_store = dcc.Store(
    id=ids.number_of_agents,
    data=initial_values.number_of_agents
)

number_of_agents_input = dcc.Input(
    id=ids.number_of_agents_input,
    type='number',
    value=initial_values.number_of_agents,
    style=style.SIDEBAR_SLIDER
)
number_of_agents_button = dbc.Button(
    'Update number of agents',
    id=ids.number_of_agents_button,
    color='primary',
    size='sm',
    style=style.SIDEBAR_BUTTON
)


def render(app: Dash, div_style: str | None = None) -> html.Div:
    @app.callback(
        Output(ids.number_of_agents, 'data'),
        Input(ids.number_of_agents_button, 'n_clicks'),
        State(ids.number_of_agents_input, 'value'),
        prevent_initial_call=True
    )
    def update_number_of_agents(n_clicks: int, number_of_agents: int) -> int:
        return number_of_agents

    return html.Div([
        number_of_agents_input,
        number_of_agents_button,
        number_of_agents_store],
        style=div_style
    )
