import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, callback

import plotly.graph_objects as go

import numpy as np
from utility import CircularBuffer
from scipy.integrate import solve_ivp
from collections import deque

''' TODO:   only have the integrator work if the plot needs more data to show (DONE)
            add button to restart integration (DONE)
            add button to perturb the system
            ability to change the dynamical system
            log scale on the y-axis
            change the integration period
            dropdown box for the number of species 
            abundance distribution
            heatmap of alpha which is modifiable
            replace mu and sigma sliders with input boxes (REVERSE?)
            add mu and sigma buttons
'''

def glv(t, y, alpha):
    return y*(1 - y + alpha@y)

REFRESH_RATE = 100 # ms

BUFFER_SIZE = 200
PLOT_WIDTH = 100 # units of dt
REINTEGRATE_THRESHOLD = 10 # re-integrate when t0 reaches here
TIME_STEPS_UNTIL_NEXT_REFRESH = 1
t0_index = 0 # zero point of the updating plot
dt = 0.1 


N = 50
sigma = 1.0
mu = 0.0
z = np.random.normal(0.0, 1.0, (N, N))
alpha = mu/N + sigma*z/np.sqrt(N)
t0 = 0.0
y0 = np.random.uniform(0, 1, N)

t = np.zeros(BUFFER_SIZE)
y = np.zeros((N, BUFFER_SIZE))
t[0] = t0
y[:, 0] = y0


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR_WIDTH = 20
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": f"{SIDEBAR_WIDTH}rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
SIDEBAR_BUTTON_STYLE = {
    'flex': '1',
    "margin-right": f"{0.01*SIDEBAR_WIDTH}rem",
    "margin-left": f"{0.01*SIDEBAR_WIDTH}rem",
    'width': f'{0.2*SIDEBAR_WIDTH}rem'
}
SIDEBAR_SLIDER_STYLE = {
    'flex': '1',
    "margin-right": f"{0.01*SIDEBAR_WIDTH}rem",
    "margin-left": f"{0.01*SIDEBAR_WIDTH}rem",
    'width': f'{0.6*SIDEBAR_WIDTH}rem'
}
HEATMAP_STYLE = {
    'width': '40rem',
    'height': '40rem',
    'margin-left': '50rem'
}


N_store = dcc.Store(id='N', data=N)
mu_store = dcc.Store(id='mu', data=mu)
sigma_store = dcc.Store(id='sigma', data=sigma)
z_store = dcc.Store(id='z', data=z)
alpha_store = dcc.Store(id='alpha', data=alpha)
y_store = dcc.Store(id='y', data=y)
t_store = dcc.Store(id='t', data=t)
t0_index_store = dcc.Store(id='t0-index', data=t0_index)

mu_input = dcc.Input(id='mu-input', type='number', value=mu, style=SIDEBAR_SLIDER_STYLE)
mu_button = dbc.Button('Update mu', id='mu-button', color='primary', size='sm', style=SIDEBAR_BUTTON_STYLE)
sigma_input = dcc.Input(id='sigma-input', type='number', value=sigma, style=SIDEBAR_SLIDER_STYLE)
sigma_button = dbc.Button('Update sigma', id='sigma-button', color='primary', size='sm', style=SIDEBAR_BUTTON_STYLE)

pause_button = dbc.Button('Pause', id='pause-button', color='primary', style=SIDEBAR_BUTTON_STYLE)
play_button = dbc.Button('Play', id='play-button', color='primary', style=SIDEBAR_BUTTON_STYLE)

reset_simulation_button = dbc.Button('Reset simulation', id='reset-simulation-button', color='primary', style=SIDEBAR_BUTTON_STYLE)

y_scale_dropdown = dcc.Dropdown(
    id='y-scale-dropdown',
    options=[
        {'label': 'Linear', 'value': 'linear'},
        {'label': 'Log', 'value': 'log'}
    ],
    value='linear',
    style=SIDEBAR_SLIDER_STYLE
)

z_reset_button = dbc.Button('Reset z', id='z-reset-button', color='primary', style=SIDEBAR_BUTTON_STYLE)

plot_updater = dcc.Interval(id='plot-updater', interval=REFRESH_RATE, n_intervals=0)

alpha_heatmap = dcc.Graph(
    id='alpha-heatmap',
    figure={
        'data': [go.Heatmap(z=alpha, colorscale='Viridis')],
        'layout': go.Layout(
            xaxis={'showticklabels': False},
            yaxis={'showticklabels': False},
        )
    },
    style=HEATMAP_STYLE
)

abundance_plot = dcc.Graph(id='abundance-plot', 
    figure={
        'data': [],
        'layout': go.Layout()
    },
    style=CONTENT_STYLE
)

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        html.Hr(),
        html.Label("mu:"),
        html.Div([mu_input, mu_button], style={'display': 'flex', 'flex-direction': 'row', 'width':'10rem'}),
        html.Hr(),
        html.Label("sigma:"),
        html.Div([sigma_input, sigma_button], style={'display': 'flex', 'flex-direction': 'row', 'width':'10rem'}),
        html.Hr(),
        html.Label("Reset z:"),
        z_reset_button,
        html.Hr(),
        html.Label("Play/Pause:"),
        html.Div([play_button, pause_button], style={'display': 'flex', 'flex-direction': 'row', 'width':'10rem'}),
        html.Hr(),
        html.Label("Reset simulation:"),
        reset_simulation_button,
        html.Hr(),
        html.Label("Y-axis scale:"),
        y_scale_dropdown,
    ],
    style=SIDEBAR_STYLE,
)


app.layout = html.Div([
    sidebar,
    abundance_plot,
    alpha_heatmap,

    N_store,
    mu_store,
    sigma_store,
    z_store,
    alpha_store,
    t0_index_store,
    t_store, 
    y_store,

    plot_updater
])

########################## UPDATE FIGURES ##########################

@callback(
    Output('alpha-heatmap', 'figure'),
    Input('alpha', 'data'),
    State('alpha-heatmap', 'figure')
)
def update_alpha_heatmap(alpha, alpha_figure):
    alpha_figure['data'][0]['z'] = alpha
    return alpha_figure

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
                        args=(alpha,), 
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


@callback(
    Output('t', 'data', allow_duplicate=True),
    Output('y', 'data', allow_duplicate=True),
    Output('t0-index', 'data', allow_duplicate=True),
    Input('alpha', 'data'),
    State('t', 'data'),
    State('y', 'data'),
    State('t0-index', 'data'),
    prevent_initial_call=True
)
def re_integrate_alpha_changed(alpha, t, y, t0_index):
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    
    sol = solve_ivp(glv, 
            (t[t0_index + PLOT_WIDTH], t[t0_index + PLOT_WIDTH] + (BUFFER_SIZE - PLOT_WIDTH)*dt), 
            y[:, t0_index + PLOT_WIDTH], 
            args=(alpha,), 
            t_eval=np.linspace(t[t0_index + PLOT_WIDTH], t[t0_index + PLOT_WIDTH] + (BUFFER_SIZE - PLOT_WIDTH)*dt, (BUFFER_SIZE - PLOT_WIDTH)), 
            atol=1e-8, rtol=1e-5)
        
    # copy the last t0_index elements of t and y to the beginning of the buffer
    # and replace the rest with the new solution
    t[:PLOT_WIDTH] = t[t0_index:t0_index + PLOT_WIDTH]
    t[PLOT_WIDTH:] = sol.t

    y[:, :PLOT_WIDTH] = y[:, t0_index:t0_index + PLOT_WIDTH]
    y[:, PLOT_WIDTH:] = sol.y[:]

    t0_index = 0

    return t, y, t0_index

########################## PLAY/PAUSE ##########################

@callback(
    Output('plot-updater', 'disabled'),
    Input('pause-button', 'n_clicks'),
)
def pause_plot(n_clicks):
    return True

@callback(
    Output('plot-updater', 'disabled', allow_duplicate=True),
    Input('play-button', 'n_clicks'),
    prevent_initial_call=True
)
def play_plot(n_clicks):
    return False

########################## RESET SIMULATION ##########################

@callback(
    Output('t', 'data', allow_duplicate=True),
    Output('y', 'data', allow_duplicate=True),
    Output('t0-index', 'data', allow_duplicate=True),
    Input('reset-simulation-button', 'n_clicks'),
    prevent_initial_call=True
)
def reset_simulation(n_clicks):
    t = np.zeros(BUFFER_SIZE)
    y = np.zeros((N, BUFFER_SIZE))
    t[0] = 0.0
    y[:, 0] = y0
    t0_index = 0
    return t, y, t0_index

########################## Y-AXIS SCALE ##########################

@callback(
    Output('abundance-plot', 'figure', allow_duplicate=True),
    Input('y-scale-dropdown', 'value'),
    State('abundance-plot', 'figure'),
    prevent_initial_call=True
)
def update_y_scale(scale, abundance_figure):
    abundance_figure['layout']['yaxis']['type'] = scale
    return abundance_figure

########################## UPDATE PARAMETERS ##########################

@callback(
    Output('alpha', 'data'),
    Input('mu', 'data'),
    Input('sigma', 'data'),
    Input('z', 'data'),
    prevent_initial_call=True
)
def update_alpha(mu, sigma, z):
    return mu/N + sigma*np.asarray(z)/np.sqrt(N)

@callback(
    Output('mu', 'data'),
    Input('mu-button', 'n_clicks'),
    State('mu-input', 'value'),
    prevent_initial_call=True
)
def update_mu(n_clicks, mu):
    return mu

@callback(
    Output('sigma', 'data'),
    Input('sigma-button', 'n_clicks'),
    State('sigma-input', 'value'),
    prevent_initial_call=True
)
def update_sigma(n_clicks, sigma):
    return sigma

@callback(
    Output('z', 'data'),
    Input('z-reset-button', 'n_clicks'),
    prevent_initial_call=True
)
def reset_z(n_clicks):
    return np.random.normal(0, 1, (N, N))

if __name__ == "__main__":
    app.run_server(debug=True)
