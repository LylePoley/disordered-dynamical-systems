
from typing import Callable, Protocol
import numpy as np

from src.components.registers import ids, types
from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
from src.components import style


# TODO: add more dynamical systems


class DisorderedDynamicalSystem(Protocol):
    id: str
    latex_equation: str

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Vector:
        """ dynamical_system(t, y, alpha) -> dy/dt """
        ...


class GeneralisedLotkaVolterra:
    id = "Generalised Lotka-Volterra"
    latex_equation = r"$$\frac{dy_i}{dt} = y_i\left(1 - y_i + \sum_j \alpha_{ij}y_j\right)$$"

    def __init__(self, r: types.Vector | float = 1.0):
        self.r = r

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Matrix:
        return y*(self.r - y + alpha@y)


class Kuramoto:
    id = "Kuramoto"
    latex_equation = r"$$\frac{dy_i}{dt} = \sum_j \alpha_{ij} \sin(y_j - y_i)$$"

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Matrix:
        return np.einsum('ij, ij -> i', alpha, np.sin(y[:, None] - y))


class SusceptibleInfectedSusceptible:
    id = "Susceptible-Infected-Susceptible"
    latex_equation = r"$$\frac{dy_i}{dt} = -y_i + (1 - y_i)\sum_j \alpha_{ij}y_j$$"

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Matrix:
        return - y + (1 - y) * alpha@y


class NeuralNetwork:
    id = "Neural Network"
    latex_equation = r"$$\frac{dy_i}{dt} = -y_i + \sum_j \alpha_{ij} \tanh(y_j)$$"

    def __init__(self, sigmoid_function: Callable = lambda x: np.tanh(x)):
        self.sigmoid_function = sigmoid_function

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Matrix:
        return -y + alpha@self.sigmoid_function(y)


dynamical_system_dropdown = dcc.Dropdown(
    options=[
        GeneralisedLotkaVolterra.id,
        Kuramoto.id,
        SusceptibleInfectedSusceptible.id,
        NeuralNetwork.id
    ],
    id=ids.dynamical_system_dropdown,
    value=GeneralisedLotkaVolterra.id,
    style=style.SIDEBAR_DROPDOWN
)

# TODO: no way for the user to input kwargs
def id_to_dynamical_system(id: str, **kwargs) -> DisorderedDynamicalSystem:

    if id == GeneralisedLotkaVolterra.id:
        return GeneralisedLotkaVolterra(**kwargs)

    elif id == Kuramoto.id:
        return Kuramoto(**kwargs)

    elif id == SusceptibleInfectedSusceptible.id:
        return SusceptibleInfectedSusceptible(**kwargs)

    elif id == NeuralNetwork.id:
        return NeuralNetwork(**kwargs)


def render(app: Dash, style: dict[str, str] | None = None) -> html.Div:

    return html.Div([
        dcc.Markdown('Dynamical system:', mathjax=True),
        dynamical_system_dropdown
        ], style=style)
