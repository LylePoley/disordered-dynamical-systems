from dash import Dash, Input, Output, html, ctx, dcc, State
import dash_bootstrap_components as dbc

from src.components import style, ids

y_scale_dropdown = dcc.Dropdown(
    id=ids.y_scale_dropdown,
    options=[
        {'label': 'Linear', 'value': 'linear'},
        {'label': 'Log', 'value': 'log'}
    ],
    value='linear',
    style=style.SIDEBAR_DROPDOWN
)

def render(app: Dash, div_style: str | None = None) -> html.Div:
    @app.callback(
        Output(ids.abundance_plot, 'figure', allow_duplicate=True),
        Input(ids.y_scale_dropdown, 'value'),
        State(ids.abundance_plot, 'figure'),
        prevent_initial_call=True
    )
    def update_y_scale(scale, abundance_figure):
        abundance_figure['layout']['yaxis']['type'] = scale
        return abundance_figure

    return html.Div([y_scale_dropdown], style=div_style)
