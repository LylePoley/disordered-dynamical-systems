import numpy as np
from typing import Annotated

Matrix = Annotated[np.ndarray, "shape: (N, N)"]
Vector = Annotated[np.ndarray, "shape: (N,)"]
OdeSolution = Annotated[np.ndarray, "shape: (N, T)"]
