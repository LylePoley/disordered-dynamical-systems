import dash
import dash_bootstrap_components as dbc
from dash import callback, Output, Input, State, html, dcc

import plotly.graph_objects as go

import numpy as np
from scipy.integrate import solve_ivp


def glv(t, y, alpha):
    return y*(1 - y + alpha@y)

REFRESH_RATE = 100 # ms

BUFFER_SIZE = 1000 # B
PLOT_WIDTH = 50 # T
REINTEGRATE_THRESHOLD = 5 # I
TIME_STEPS_UNTIL_NEXT_REFRESH = 1
t0_index = 0
dt = 0.1

N = 2
mu = -1.0
sigma = 1.0
z = np.random.normal(0.0, 1.0, (N, N))
t0_index = 0
t0 = 0.0
y0 = np.array([2.0, 1.0])
alpha0 = np.array([[0.0, -1.0], [-0.5, 0.0]])

t = np.zeros(BUFFER_SIZE, dtype=float)
y = np.zeros((N, BUFFER_SIZE), dtype=float)
t[0] = t0
y[:, 0] = y0

N = dcc.Store(id='N', data=N)
mu = dcc.Store(id='mu', data=mu)
sigma = dcc.Store(id='sigma', data=sigma)
z = dcc.Store(id='z', data=z)
alpha = dcc.Store(id='alpha', data=alpha)
t0_index = dcc.Store(id='t0-index', data=t0_index)

mu_input = dcc.Input(id='mu-input', type='number', value=mu0, style=SIDEBAR_SLIDER_STYLE)
mu_button = dbc.Button('Update mu', id='mu-button', color='primary', size='sm', style=SIDEBAR_BUTTON_STYLE)
sigma_input = dcc.Input(id='sigma-input', type='number', value=sigma0, style=SIDEBAR_SLIDER_STYLE)
sigma_button = dbc.Button('Update sigma', id='sigma-button', color='primary', size='sm', style=SIDEBAR_BUTTON_STYLE)

z_reset_button = dbc.Button('Reset z', id='z-reset-button', color='primary', style=SIDEBAR_BUTTON_STYLE)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

abundance_plot = dcc.Graph(
    id='abundance-plot', 
    figure={
        'data': [], 
        'layout': go.Layout()
    }
)
alpha_store = dcc.Store(id='alpha', data=alpha0)
t0_index_store = dcc.Store(id='t0-index', data=t0_index)
t_store = dcc.Store(id='t', data=t)
y_store = dcc.Store(id='y', data=y)
plot_updater = dcc.Interval(id='plot-updater', interval=100, n_intervals=0)



app.layout = html.Div([
    abundance_plot,
    alpha_store,
    t0_index_store,
    t_store,
    y_store,
    plot_updater
])

@callback(
    [Output('t', 'data'), Output('y', 'data'), Output('abundance-plot', 'figure'), Output('t0-index', 'data')],
    [Input('plot-updater', 'n_intervals')],
    [State('t', 'data'), State('y', 'data'), 
     State('abundance-plot', 'figure'), State('t0-index', 'data'), State('alpha', 'data')]
)
def update_abundance_plot(n_intervals, t, y, abundance_figure, t0_index, alpha):
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)

    if t[t0_index] == 0.0:
        sol = solve_ivp(glv, 
                        (0.0, 0.0 + BUFFER_SIZE*dt), 
                        y0, 
                        args=(alpha0,), 
                        t_eval=np.linspace(0.0, 0.0 + BUFFER_SIZE*dt, BUFFER_SIZE), 
                        atol=1e-8, rtol=1e-5)
        
        t = sol.t
        y = sol.y

        t0_index = 0
        abundance_figure['data'] = [go.Scatter(
            x=t[t0_index:t0_index + PLOT_WIDTH], 
            y=y[i, t0_index:t0_index + PLOT_WIDTH],
              mode='lines', showlegend=False) for i in range(N)]

        return t, y, abundance_figure, t0_index + TIME_STEPS_UNTIL_NEXT_REFRESH

    if t0_index + PLOT_WIDTH + REINTEGRATE_THRESHOLD >= BUFFER_SIZE:
        sol = solve_ivp(glv, 
                        (t[-1], t[-1] + t0_index*dt), 
                        y[:, -1], 
                        args=(alpha,), 
                        t_eval=np.linspace(t[-1], t[-1] + t0_index*dt, t0_index), 
                        atol=1e-8, rtol=1e-5)
        
        # copy the last t0_index elements of t and y to the beginning of the buffer
        # and replace the rest with the new solution
        t[:-t0_index] = t[t0_index:]
        y[:, :-t0_index] = y[:, t0_index:]
        t[-t0_index:] = sol.t
        y[:, -t0_index:] = sol.y[:]

        t0_index = 0

    abundance_figure['data'] = [go.Scatter(
                                x=t[t0_index:t0_index + PLOT_WIDTH], 
                                y=y[i, t0_index:t0_index + PLOT_WIDTH],
                                mode='lines', 
                                showlegend=False) for i in range(N)]
    
    return t, y, abundance_figure, t0_index + TIME_STEPS_UNTIL_NEXT_REFRESH

####################### UPDATING PARAMETERS #######################


@callback(
    Output('alpha', 'data'),
    Input('mu', 'data'),
    Input('sigma', 'data'),
    Input('z', 'data'),
    prevent_initial_call=True
)
def update_alpha(mu, sigma, z):
    return mu/N0 + sigma*np.asarray(z)/np.sqrt(N0)

@callback(
    Output('mu', 'data'),
    Input('mu-input', 'value'),
    prevent_initial_call=True
)
def update_mu(mu):
    return mu

@callback(
    Output('sigma', 'data'),
    Input('sigma-input', 'value'),
    prevent_initial_call=True
)
def update_sigma(sigma):
    return sigma

@callback(
    Output('z', 'data'),
    Input('z-reset-button', 'n_clicks'),
    prevent_initial_call=True
)
def reset_z(n_clicks):
    print('z-reset')
    return np.random.normal(0, 1, (N0, N0))


if __name__ == "__main__":
    app.run_server(debug=True)
