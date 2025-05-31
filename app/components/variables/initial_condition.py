from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import numpy as np

from constants import ids, initial_values, types

from text.tooltips import initial_condition as tooltip_text

initial_condition_store = dcc.Store(
    id=ids.initial_condition,
    data=initial_values.y0
)

initial_condition_reset_button = dbc.Button(
    'Re-draw initial condition',
    id=ids.initial_condition_reset_button,
    color='primary',
)

initial_condition_reset_tooltip = dbc.Tooltip(
    [
        dcc.Markdown(
            tooltip_text,
            mathjax=True)],
    target=ids.initial_condition_reset_button
)

def render(app: Dash, class_name: str | None = None) -> html.Div:
    @app.callback(
        Output(ids.initial_condition, 'data'),
        Input(ids.initial_condition_reset_button, 'n_clicks'),
        State(ids.number_of_agents_input, 'value'),
        prevent_initial_call=True
    )
    def reset_interaction_noise(n_clicks: int, number_of_agents: int) -> types.Matrix:
        return np.random.uniform(0, 1, number_of_agents)


    return html.Div([
        initial_condition_reset_button,
        initial_condition_store,
        initial_condition_reset_tooltip],
        className=class_name
        )
