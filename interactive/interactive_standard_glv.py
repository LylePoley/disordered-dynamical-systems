

import dash
import dash_bootstrap_components as dbc
from dash import (dcc, html)

from src.components.variables import (
    dynamical_system,
    interaction_matrix,
    interaction_mean,
    interaction_noise,
    interaction_standard_deviation,
    number_of_agents,
    time_final,
    time,
    y,
)

from src.components.plots import (
    trajectories
)

from src.components.registers import (
    ids,
    initial_values
)

from src.components import (
    style,
    integration
)

''' TODO:   only have the integrator work if the plot needs more data to show (DONE)
            add button to restart integration (DONE)
            add button to perturb the system 
            ability to change the dynamical system (DONE)
            log scale on the y-axis (DONE)
            abundance distribution (PARTIALLY DONE)
            heatmap of alpha which is modifiable 
            replace mu and sigma sliders with input boxes (DONE)
            add mu and sigma buttons (DONE)
            register the id of a component within the file that the component is defined in (NOT GOING TO DO)
            make a function to add to the ids file if a new component is added, but to do nothing otherwise (NOT GOING TO DO)
'''


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

sidebar = html.Div(
    [
        html.H3("Options", className="display-4"),
        html.Hr(),
        html.P(
            "Select options for the integration.", className="lead"
        ),
        html.Hr(),
        interaction_mean.render(
            app, div_style=style.SIDEBAR_DIV),

        html.Hr(),
        interaction_standard_deviation.render(
            app, div_style=style.SIDEBAR_DIV),

        html.Hr(),
        number_of_agents.render(
            app, div_style=style.SIDEBAR_DIV),

        html.Hr(),
        time_final.render(app, div_style=style.SIDEBAR_DIV),

        html.Hr(),
        interaction_noise.render(app, div_style=style.SIDEBAR_DIV),

        html.Hr(),
        integration.render(app, div_style=style.SIDEBAR_DIV),

        html.Hr(),
        html.Label("Dynamical system:", style=style.SIDEBAR_DIV),
        dynamical_system.render(app, div_style=style.SIDEBAR_DIV)
    ],
    style=style.SIDEBAR,
)


app.layout = html.Div([
    sidebar,
    trajectories.render(app),

    interaction_matrix.render(app),
    time.render(),
    y.render(),
])


if __name__ == "__main__":
    app.run_server(debug=True)
