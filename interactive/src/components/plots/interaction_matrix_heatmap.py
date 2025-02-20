""" Figure of the solutions to the dynamical system within the given time interval."""

from dash import Dash, Input, Output, State, dcc

import plotly.graph_objects as go
import plotly.express as px
from src.components.registers import ids, initial_values, types

def render(app: Dash, class_name: str | None = None) -> dcc.Graph:
    @app.callback(
        Output(ids.interaction_matrix_heatmap, 'figure'),
        Input(ids.interaction_matrix, 'data'),
        State(ids.interaction_matrix_heatmap, 'figure'),
    )
    def update_abundance_plot_data(
        interaction_matrix: types.Matrix,
        interaction_matrix_heatmap: go.Figure
    ) -> go.Figure:

        interaction_matrix_heatmap['data'][0]['z'] = interaction_matrix
        return interaction_matrix_heatmap

    return dcc.Graph(
        id=ids.interaction_matrix_heatmap,
        figure=px.imshow(
            initial_values.interaction_matrix,
            color_continuous_scale='Viridis',
            aspect='equal'
        ).update_layout(
            coloraxis_showscale=False,
            xaxis_showticklabels=False,
            yaxis_showticklabels=False,
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            margin=dict(l=0, r=0, t=0, b=0),  # Reduce padding around the figure
            autosize=True,  # Enable autosizing
            # plot_bgcolor='black',  # Set background color to black
            # paper_bgcolor='black'  # Set paper background color to black
        ),
        style={'width': '100%', 'height': '100%'}  # Set the style to make the graph responsive
    )
    # return dcc.Graph(
    #     id=ids.interaction_matrix_heatmap,
    #     figure={
    #         'data': [go.Heatmap(z=initial_values.interaction_matrix, colorscale='Viridis', showscale=False)],
    #         'layout': go.Layout(
    #             xaxis={'showticklabels': False, 'showgrid': False, 'zeroline': False, 'scaleanchor': 'y', 'scaleratio': 1, 'ticks': ''},
    #             yaxis={'showticklabels': False, 'showgrid': False, 'zeroline': False, 'scaleanchor': 'x', 'scaleratio': 1, 'ticks': ''},
    #             margin=dict(l=0, r=0, t=0, b=0),  # Reduce padding around the figure
    #             autosize=True,  # Enable autosizing
    #             # width=100,  # Set the width of the figure to be relative
    #             # height=100  # Set the height of the figure to be relative
    #         )
    #     },
    #     style={'width': '100%', 'height': '100%'}  # Set the style to make the graph responsive
    # )
