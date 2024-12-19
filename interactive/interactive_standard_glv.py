import numpy as np
from scipy.integrate import solve_ivp, RK45
import dash
from dash import dcc, html, ctx, callback, Input, Output, State
import dash.dependencies as dd
import plotly.graph_objs as go
import custom_components as cc
from functools import partial
from collections import deque
from jsonpickle import encode, decode
from utility import *

def glv(t, y, alpha):
    dydt = y * (1 - y + alpha @ y)
    return dydt


N = 50  # Example size
sigma = 1.0
mu = 0.0
perturbation = np.random.normal(0, 1/np.sqrt(N), N)
z = np.random.normal(0, 1, (N, N))
alpha = mu/N + sigma*z/np.sqrt(N)

y0 = np.random.uniform(0, 1, N)
t = deque(maxlen=100)
y = deque(maxlen=100)

glv_bound = partial(glv, alpha=alpha)
solver_state = RK45_state(glv_bound, 0, y0, np.inf, rtol=1e-4, atol=1e-5, max_step=0.2)
# solver = RK45(glv_bound, 0, y0, np.inf, max_step=0.2)

app = dash.Dash(__name__)

mu_slider = cc.SliderDiv(id='mu-slider', label=r'$\mu$', min=-5, max=5, step=0.01, value=0.0)
sigma_slider = cc.SliderDiv(id='sigma-slider', label=r'$\sigma$', min=0, max=2, step=0.01, value=1.0)

N_dropdown = dcc.Dropdown(
    id='N-dropdown',
    options=[{'label': str(i), 'value': i} for i in [1, 2, 5, 10, 25, 50, 100]],
    value=N,
    clearable=False,
    style={'margin': '10px'}
)

abundances_figure = dcc.Graph(id='abundances', mathjax=True, figure={'data': [go.Scatter(x=[], y=[], mode='lines')], 'layout': {'title': 'Abundances'}})

heatmap_figure = dcc.Graph(id='heatmap', mathjax=True,
                           figure={'data': [go.Heatmap(z=sigma*z, colorscale='Viridis', colorbar={'xpad': 0})],
                                   'layout': {'title': r'Heatmap of $\alpha$',
                                            'xaxis': {'scaleanchor': 'y', 'constrain': 'domain', 'showticklabels': False, 'ticks': ''},
                                            'yaxis': {'constrain': 'domain', 'showticklabels': False, 'ticks': ''}
                                   }
                           }
)



restart_button = cc.ButtonDiv(id='restart-button', label=r'Restart simulation', style={'margin': '10px'})
regenerate_z_button = cc.ButtonDiv(id='regenerate-z-button', label=r'Re-generate $\alpha$', style={'margin': '10px'})
perturb_button = cc.ButtonDiv(id='perturb-button', label=r'Perturb', style={'margin': '10px'})

app.layout = html.Div(children=[
    html.H1(children='Differential Equation Solutions'),

    # Abundances figure at the top
    html.Div([
        abundances_figure,
        restart_button,
        regenerate_z_button,
        perturb_button
    ], style={'display': 'flex', 'flex-direction': 'column'}),

    # Heatmap and sliders below
    html.Div([
        html.Div([
            heatmap_figure,
            html.Div([mu_slider, sigma_slider], style={'display': 'flex', 'flex-direction': 'column', 'flex-grow': '1', 'margin': '10px'})
        ], style={'display': 'flex', 'flex-direction': 'row', 'flex-grow': '1', 'margin': '10px', 'align-items': 'center'})
    ], style={'display': 'flex', 'flex-direction': 'column', 'flex-grow': '1', 'margin': '10px'}),

    dcc.Store(id='alpha', data=alpha),
    dcc.Store(id='z', data=z),
    dcc.Store(id='solver', data=encode(solver_state)),
    dcc.Store(id='fun', data=encode(glv_bound)),
    dcc.Store(id='mu', data=mu),
    dcc.Store(id='sigma', data=sigma),
    dcc.Store(id='apply-perturbation', data=False),
    dcc.Interval(id='rk-update', interval=1*300, n_intervals=0)
])

# @callback(
#         Output
# )

@callback(
    Output('heatmap', 'figure'),
    Input('alpha', 'data'),
    State('heatmap', 'figure')
)
def update_heatmap(alpha, heatmap_figure):
    heatmap_figure['data'] = [go.Heatmap(z=alpha, colorscale='Viridis')]

    return heatmap_figure




@callback(
    Output('abundances', 'figure'),
    Output('solver', 'data'),
    Input('rk-update', 'n_intervals'),
    State('abundances', 'figure'),
    State('solver', 'data'),
    State('alpha', 'data'),
    State('apply-perturbation', 'data')
)
def redraw_graph(n_intervals, abundances_figure, solver_state, alpha, apply_perturbation):
    solver_state = decode(solver_state)

    step(partial(glv, alpha=alpha), solver_state)
    if apply_perturbation:
        solver_state['y'] += perturbation

    t.append(solver_state['t'])
    y.append(solver_state['y'])

    abundances_figure['data'] = [
        go.Scatter(x=np.asarray(t), y=np.asarray(y)[:, i], mode='lines', showlegend=False) for i in range(N)
    ]

    return abundances_figure, encode(solver_state)


######################################## KEEPING TRACK OF PARAMETERS ########################################



@callback(
        Output('apply-perturbation', 'data'),
        Input('perturb-button', 'n_clicks'),
        State('apply-perturbation', 'data')
)
def apply_perturbation(n_clicks, apply_perturbation):
    return not apply_perturbation

@callback(
        Output('alpha', 'data'),
        Input('mu', 'data'),
        Input('sigma', 'data'),
        Input('z', 'data')
)
def update_alpha(mu, sigma, z):
    return mu/N + sigma*np.asarray(z)/np.sqrt(N)

@callback(
        Output('z', 'data'),
        Input('regenerate-z-button', 'n_clicks')
)
def reset_z(n_clicks):
    z = np.random.normal(0, 1, (N, N))
    return z

@callback(
        Output('mu', 'data'),
        Input('mu-slider', 'value')
)
def update_mu(mu):
    return mu

@callback(
        Output('sigma', 'data'),
        Input('sigma-slider', 'value')
)
def update_sigma(sigma):
    return sigma


if __name__ == '__main__':
    app.run_server(debug=True)
