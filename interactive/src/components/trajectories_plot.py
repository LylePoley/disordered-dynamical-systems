from dash import Dash, Input, Output, State, dcc, callback

import plotly.graph_objects as go
from src.components import style, ids, initial_values, constants


def render(app: Dash) -> dcc.Graph:
    @app.callback(
            Output(ids.abundance_plot, 'figure'),
            Input(ids.t0_index, 'data'),
            State(ids.abundance_plot, 'figure'), 
            State(ids.t, 'data'), 
            State(ids.y, 'data')
    )
    def update_abundance_plot_data(t0_index, abundance_figure, t, y):
        '''
        Plot the data from t0_index to t0_index + PLOT_WIDTH
        '''
        for i in range(initial_values.N):
            abundance_figure['data'][i]['x'] = t[t0_index:t0_index + constants.PLOT_WIDTH]
            abundance_figure['data'][i]['y'] = y[i][t0_index:t0_index + constants.PLOT_WIDTH]

        return abundance_figure

    return dcc.Graph(id=ids.abundance_plot, 
        figure={
            'data': [go.Scatter(x=[], y=[], mode='lines', showlegend=False) for _ in range(initial_values.N)],
            'layout': go.Layout(xaxis={'title': 'Time'})
        },
        style=style.CONTENT
    )