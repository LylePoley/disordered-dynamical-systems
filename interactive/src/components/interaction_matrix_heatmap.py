from dash import Dash, Input, Output, State, dcc, callback

import plotly.graph_objects as go
from src.components import style, ids, initial_values


def render(app: Dash) -> dcc.Graph:
    @app.callback(
        Output(ids.alpha_heatmap, 'figure'),
        Input(ids.alpha, 'data'),
        State(ids.alpha_heatmap, 'figure')
    )
    def update_alpha_heatmap(alpha, alpha_figure):
        alpha_figure['data'][0]['z'] = alpha
        return alpha_figure

    return dcc.Graph(
        id=ids.alpha_heatmap,
        figure={
            'data': [go.Heatmap(z=initial_values.alpha, colorscale='Viridis')],
            'layout': go.Layout(
                xaxis={'showticklabels': False},
                yaxis={'showticklabels': False},
            )
        },
        style=style.HEATMAP
    )