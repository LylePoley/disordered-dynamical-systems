import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, callback, ctx

# from interactive.src.components import dynamical_system_dropdown
from src.components.variables import (
    dynamical_system,
    mu, 
    sigma, 
    alpha, 
    z, 
    t0_index
)

from src.components import (
    ids,
    initial_values,
    style, 
    interaction_matrix_heatmap, 
    trajectories_plot, 
    play_pause_button, 
    reset_simulation_button, 
    automatic_re_integration, 
    y_scale_dropdown,
    abundance_histogram,
    constants
)

''' TODO:   only have the integrator work if the plot needs more data to show (DONE)
            add button to restart integration (DONE)
            add button to perturb the system 
            ability to change the dynamical system
            log scale on the y-axis (DONE)
            change the integration period 
            dropdown box for the number of species 
            abundance distribution 
            heatmap of alpha which is modifiable
            replace mu and sigma sliders with input boxes (REVERSE?)
            add mu and sigma buttons
            register the id of a component within the file that the component is defined in,
            make a function to add to the ids file if a new component is added, but to do nothing otherwise
'''
# glv = dynamical_system.GeneralisedLotkaVolterra()
glv = dynamical_system.NeuralNetwork()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

N_store = dcc.Store(id=ids.N, data=constants.N)
y_store = dcc.Store(id=ids.y, data=initial_values.y)
t_store = dcc.Store(id=ids.t, data=initial_values.t)

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        html.Hr(),
        html.Label("mu:"),
        mu.render(app, div_style=style.SIDEBAR_DIV),

        html.Hr(),
        html.Label("sigma:"),
        sigma.render(app, div_style=style.SIDEBAR_DIV),

        html.Hr(),
        html.Label("Reset z:"),
        z.render(app, div_style=style.SIDEBAR_DIV),

        html.Hr(),
        html.Label("Play/Pause:"),
        play_pause_button.render(app, div_style=style.SIDEBAR_DIV),

        html.Hr(),
        html.Label("Reset simulation:"),
        reset_simulation_button.render(app, div_style=style.SIDEBAR_DIV),
        
        # html.Hr(),
        # html.Label("Y-axis scale:"),
        # y_scale_dropdown.render(app, div_style=style.SIDEBAR_DIV),
    ],
    style=style.SIDEBAR,
)


app.layout = html.Div([
    sidebar,
    trajectories_plot.render(app),
    # interaction_matrix_heatmap.render(app),
    abundance_histogram.render(app),

    N_store,
    alpha.render(app),
    t0_index.render(app),
    t_store, 
    y_store,
    automatic_re_integration.render(app, glv)
])


if __name__ == "__main__":
    app.run_server(debug=True)
