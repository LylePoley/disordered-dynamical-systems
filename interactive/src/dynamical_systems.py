
from typing import Callable, Protocol
import numpy as np

class DisorderedDynamicalSystem(Protocol):
    """ dynamical_system(t, y, alpha) -> dy/dt """
    def __call__(self, t: float, y: np.ndarray, alpha: np.ndarray) -> np.ndarray:
        ...


class GeneralisedLotkaVolterra(DisorderedDynamicalSystem):
    def __init__(self, r: np.ndarray | float = 1.0):
        self.r = r

    def __call__(self, t: float, y: np.ndarray, alpha: np.ndarray) -> np.ndarray:
        return y*(self.r - y + alpha@y)
    
class Kuramoto(DisorderedDynamicalSystem):
    def __call__(self, t: float, y: np.ndarray, alpha: np.ndarray) -> np.ndarray:
        return alpha@np.sin(y[:, None] - y)
    
class SusceptibleInfectedSusceptible(DisorderedDynamicalSystem):
    def __call__(self, t: float, y: np.ndarray, alpha: np.ndarray) -> np.ndarray:
        return - y + (1 - y) * alpha@y
    
class NeuralNetwork(DisorderedDynamicalSystem):
    def __init__(self, sigmoid_function: Callable = lambda x: np.tanh(x)):
        self.sigmoid_function = sigmoid_function

    def __call__(self, t: float, y: np.ndarray, alpha: np.ndarray) -> np.ndarray:
        return -y + alpha@self.sigmoid_function(y)

# TODO: add more dyamical systems
# TODO: allow changing the parameters of the dynamical system
disordered_dynamical_systems = {
    'Generalised Lotka-Volterra': GeneralisedLotkaVolterra(),
    'Kuramoto': Kuramoto(),
    'Susceptible-Infected-Susceptible': SusceptibleInfectedSusceptible(),
    'Neural Network': NeuralNetwork()
}

def id_to_dynamical_system(id: str) -> DisorderedDynamicalSystem:
    return disordered_dynamical_systems[id]