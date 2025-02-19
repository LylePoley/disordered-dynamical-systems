""" Figure of the solutions to the dynamical system within the given time interval."""

from dash import Dash, Input, Output, State, dcc

import plotly.graph_objects as go
from src.components.registers import ids, initial_values, types
from src.components import style

def make_figure(t: types.Vector | list = [], y: types.OdeSolution | list = []) -> go.Figure:
    fig = go.Figure()

    for yi in y:
        fig.add_trace(go.Scatter(x=t, y=yi, mode='lines', showlegend=False))
    fig.update_layout(
        xaxis_title='Time',
        xaxis_rangeslider_visible=True,
        yaxis_title= r"agent state",
        yaxis_fixedrange=False)

    return fig

def render(app: Dash, style: dict[str, str] | None = None) -> dcc.Graph:
    @app.callback(
        Output(ids.abundance_plot, 'figure'),
        Input(ids.time, 'data'),
        Input(ids.y, 'data'),
        State(ids.abundance_plot, 'figure'),
    )
    def update_abundance_plot_data(
        t: float,
        y: types.Vector,
        abundance_figure: go.Figure
        )\
            -> go.Figure:
        
        fig = make_figure(t, y)

        return fig

    # initial creation of the figure
    fig = make_figure()

    return dcc.Graph(id=ids.abundance_plot,
                     figure=fig,
                     style=style
                     )
