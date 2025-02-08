
from typing import Callable, Protocol
import numpy as np

from src.components.registers import ids, types


from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from src.components import style

from enum import IntEnum

# TODO: add more dynamical systems


class DisorderedDynamicalSystem(Protocol):
    label: str
    markdown_description: str

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Vector:
        """ dynamical_system(t, y, alpha) -> dy/dt """
        ...


class GeneralisedLotkaVolterra:
    label = ids.generalised_lotka_volterra
    makrdown_description = ""

    def __init__(self, r: types.Vector | float = 1.0):
        self.r = r

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Matrix:
        return y*(self.r - y + alpha@y)


class Kuramoto:
    label = ids.kuramoto
    makrdown_description = ""

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Matrix:
        return np.einsum('ij, ij -> i', alpha, np.sin(y[:, None] - y))


class SusceptibleInfectedSusceptible:
    label = ids.susceptible_infected_susceptible
    makrdown_description = ""

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Matrix:
        return - y + (1 - y) * alpha@y


class NeuralNetwork:
    label = ids.neural_network
    makrdown_description = ""

    def __init__(self, sigmoid_function: Callable = lambda x: np.tanh(x)):
        self.sigmoid_function = sigmoid_function

    def __call__(self, t: float, y: types.Vector, alpha: types.Matrix) -> types.Matrix:
        return -y + alpha@self.sigmoid_function(y)


# dynamical_systems =

class AvailableSystem(IntEnum):
    GENERALISED_LOTKA_VOLTERRA = 0
    KURAMOTO = 1
    SUSCEPTIBLE_INFECTED_SUSCEPTIBLE = 2
    NEURAL_NETWORK = 3


dynamical_system_dropdown = dcc.Dropdown(
    options=[
        {'label': GeneralisedLotkaVolterra.label,
            'value': AvailableSystem.GENERALISED_LOTKA_VOLTERRA.value},
        {'label': Kuramoto.label, 'value': AvailableSystem.KURAMOTO.value},
        {'label': SusceptibleInfectedSusceptible.label,
            'value': AvailableSystem.SUSCEPTIBLE_INFECTED_SUSCEPTIBLE.value},
        {'label': NeuralNetwork.label, 'value': AvailableSystem.NEURAL_NETWORK.value}
    ],
    id=ids.dynamical_system_dropdown,
    value=AvailableSystem.GENERALISED_LOTKA_VOLTERRA.value,
    style=style.SIDEBAR_DROPDOWN
)

# TODO: no way for the user to input kwargs
def id_to_dynamical_system(id: int, **kwargs) -> DisorderedDynamicalSystem:

    if id == AvailableSystem.GENERALISED_LOTKA_VOLTERRA.value:
        return GeneralisedLotkaVolterra(**kwargs)

    elif id == AvailableSystem.KURAMOTO.value:
        return Kuramoto(**kwargs)

    elif id == AvailableSystem.SUSCEPTIBLE_INFECTED_SUSCEPTIBLE.value:
        return SusceptibleInfectedSusceptible(**kwargs)

    elif id == AvailableSystem.NEURAL_NETWORK.value:
        return NeuralNetwork(**kwargs)


def render(app: Dash, div_style: str | None = None) -> html.Div:

    return html.Div([dynamical_system_dropdown], style=div_style)
