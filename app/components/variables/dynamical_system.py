
from typing import Callable, Protocol
import numpy as np

from constants import ids, types
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# TODO: add more dynamical systems
# TODO: add descriptions to each system to put into tooltips

class DisorderedDynamicalSystem(Protocol):
    id: str
    latex_equation: str
    description: str

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Vector:
        """ dynamical_system(t, y, alpha) -> dy/dt """
        ...


class GeneralisedLotkaVolterra:
    id = "Generalised Lotka-Volterra"
    latex_equation = r'$$\frac{dy_i}{dt} = y_i\left(1 - y_i + \sum_j \alpha_{ij}y_j\right)$$'
    description = "The generalised Lotka-Volterra model describes the abundances $y_i$ of $N$ species in an ecosystem. "

    def __init__(self, r: types.Vector | float = 1.0):
        self.r = r

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Matrix:
        return y*(self.r - y + alpha@y)


class Kuramoto:
    id = "Kuramoto"
    latex_equation = r"$$\frac{dy_i}{dt} = \sum_j \alpha_{ij} \sin(y_j - y_i)$$"
    description = ""

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Vector:
        return np.einsum('ij, ij -> i', alpha, np.sin(y[:, None] - y))


class SusceptibleInfectedSusceptible:
    id = "Susceptible-Infected-Susceptible"
    latex_equation = r"$$\frac{dy_i}{dt} = -y_i + (1 - y_i)\sum_j \alpha_{ij}y_j$$"
    description = ""

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Vector:
        return - y + (1 - y) * alpha@y


class NeuralNetwork:
    id = "Neural Network"
    latex_equation = r"$$\frac{dy_i}{dt} = -y_i + \sum_j \alpha_{ij} \tanh(y_j)$$"
    description = ""

    def __init__(self, sigmoid_function: Callable = lambda x: np.tanh(x)):
        self.sigmoid_function = sigmoid_function

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Vector:
        return -y + alpha@self.sigmoid_function(y)

class Linear:
    id = "Linear"
    latex_equation = r"$$\frac{dy_i}{dt} = -y_i + \sum_j \alpha_{ij}y_j$$"
    description = ""

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Vector:
        return -y + alpha@y

# TODO: allow user to change the args and kwargs for each dynamical system, currently, they only take their default values
def id_to_dynamical_system(id: str, *args, **kwargs) -> DisorderedDynamicalSystem:

    if id == GeneralisedLotkaVolterra.id:
        return GeneralisedLotkaVolterra(*args, **kwargs)

    elif id == Kuramoto.id:
        return Kuramoto(*args, **kwargs)

    elif id == SusceptibleInfectedSusceptible.id:
        return SusceptibleInfectedSusceptible(*args, **kwargs)

    elif id == NeuralNetwork.id:
        return NeuralNetwork(*args, **kwargs)

    elif id == Linear.id:
        return Linear(*args, **kwargs)


dynamical_system_dropdown = dcc.Dropdown(
    options=[
        GeneralisedLotkaVolterra.id,
        Kuramoto.id,
        SusceptibleInfectedSusceptible.id,
        NeuralNetwork.id,
        Linear.id
    ],
    id=ids.dynamical_system_dropdown,
    value=GeneralisedLotkaVolterra.id
)

dynamical_system_tooltip = dbc.Tooltip(
    """Select which dynamical system to integrate.
    On pressing the 'integrate' button, the selected
    dynamical system will be integrated and the results displayed.""",
    target=ids.dynamical_system_dropdown,
)

def render(app: Dash, class_name: str | None = None) -> html.Div:

    return html.Div([
        dcc.Markdown('Dynamical system:', mathjax=True),
        dynamical_system_dropdown,
        dynamical_system_tooltip
    ], className=class_name)
