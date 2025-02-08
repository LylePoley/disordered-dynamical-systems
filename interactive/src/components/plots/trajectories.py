""" Figure of the solutions to the dynamical system within the given time interval."""

from dash import Dash, Input, Output, State, dcc

import plotly.graph_objects as go
from src.components.registers import ids, initial_values, types
from src.components import style


def render(app: Dash) -> dcc.Graph:
    @app.callback(
        Output(ids.abundance_plot, 'figure'),
        Input(ids.time, 'data'),
        Input(ids.y, 'data'),
        State(ids.abundance_plot, 'figure'),
        State(ids.number_of_agents, 'data'),
    )
    def update_abundance_plot_data(t: float, y: types.Vector, abundance_figure: go.Figure, number_of_agents: int) -> go.Figure:
        for i in range(number_of_agents):
            abundance_figure['data'][i]['x'] = t
            abundance_figure['data'][i]['y'] = y[i]

        return abundance_figure

    # initial creation of the figure
    fig = go.Figure()
    for _ in range(initial_values.number_of_agents):
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', showlegend=False))
    fig.update_layout(xaxis={'title': 'Time'})
    fig.update_layout(
        yaxis=dict(
            autorange=True,
            fixedrange=False
        )
    )
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            )
        )
    )

    return dcc.Graph(id=ids.abundance_plot,
                     figure=fig,
                     style=style.CONTENT
                     )
