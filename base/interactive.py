'''
'''

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
from scipy.integrate import RK45
from circular_buffer import CircularBuffer

def dydt(t, y):
    return np.sin(t)

initial_time = 0
initial_value = [0.5] 
solver = RK45(dydt, initial_time, initial_value, t_bound=500, max_step=0.01)

times = CircularBuffer(50)
values = CircularBuffer(50)
times.append(initial_time)
values.append(initial_value[0])
# times = [initial_time]
# values = [initial_value[0]]

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, 
        n_intervals=0
    ),
    dcc.Input(id='interval-input', type='number', placeholder='Interval (ms)', value=100),
    html.Button('Set Interval', id='set-interval-button', n_clicks=0),
    html.Div(id='current-step', children='Current Step: 0')
])

@app.callback(
    Output('interval-component', 'interval'),
    [Input('set-interval-button', 'n_clicks')],
    [State('interval-input', 'value')]
)
def update_interval(n_clicks, value):
    return value if value else 1000

@app.callback(
    [Output('graph', 'figure'),
     Output('current-step', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n_intervals):
    global solver, times, values
    if solver.status == 'running':
        solver.step()
        times.append(solver.t)
        values.append(solver.y[0])

    fig = go.Figure(data=[go.Scatter(x=times.buffer, y=values.buffer, mode='markers')])
    fig.update_layout(xaxis=dict(showticklabels=False))
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False, yaxis_showline=False)
    fig.update_layout(title='RK45 Solution', xaxis_title='Time', yaxis_title='Value')

    
    return fig, f'Current Step: {len(times.get()) - 1}'

if __name__ == '__main__':
    app.run_server(debug=True)
