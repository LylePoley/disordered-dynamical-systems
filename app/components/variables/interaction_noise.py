from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import numpy as np

from constants import ids, initial_values, types
from components.plots import interaction_matrix_heatmap

z_store = dcc.Store(
    id=ids.interaction_noise,
    data=initial_values.interaction_noise
)

z_reset_button = dbc.Button(
    'Re-draw noise',
    id=ids.interaction_noise_reset_button,
    color='primary',
)


def render(app: Dash, class_name: str | None = None) -> html.Div:
    @app.callback(
        Output(ids.interaction_noise, 'data'),
        Input(ids.interaction_noise_reset_button, 'n_clicks'),
        State(ids.number_of_agents_input, 'value'),
        prevent_initial_call=True
    )
    def reset_interaction_noise(n_clicks: int, number_of_agents: int) -> types.Matrix:
        return np.random.normal(0, 1, (number_of_agents, number_of_agents))

    z_reset_tooltip = dbc.Tooltip(
        [
            dcc.Markdown(
                r"""Re-generates the interaction coefficients $\alpha_{ij}$
                from a Gaussian distribution with mean $\frac{\mu}{N}$ and
                variance $\frac{\sigma^2}{N}$. Below is a heatmap of the
                interaction matrix.""",
                mathjax=True),
            html.Div([interaction_matrix_heatmap.render(app)], className="heatmap-tooltip")],
        target=ids.interaction_noise_reset_button
    )

    return html.Div([z_reset_button, z_store, z_reset_tooltip], className=class_name)
