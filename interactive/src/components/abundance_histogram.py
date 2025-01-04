from dash import Dash, Input, Output, State, dcc, callback

import plotly.graph_objects as go
from src.components import style, ids, initial_values, constants


def render(app: Dash) -> dcc.Graph:
    @app.callback(
            Output(ids.abundance_histogram, 'figure'),
            Input(ids.t0_index, 'data'),
            State(ids.abundance_histogram, 'figure'), 
            State(ids.t, 'data'), 
            State(ids.y, 'data')
    )
    def update_abundance_histogram_data(t0_index, abundance_figure, t, y):
        '''
        Plot the data from t0_index to t0_index + PLOT_WIDTH
        '''
        for i in range(initial_values.N):
            abundance_figure['data'][0]['x'] = [abundance[t0_index + constants.PLOT_WIDTH] for abundance in y] 

        return abundance_figure


    return dcc.Graph(id=ids.abundance_histogram, 
        figure={
            'data': [go.Histogram(x=[])],
            'layout': go.Layout()
        },
        style=style.CONTENT
    )