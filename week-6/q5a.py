from typing import Optional
import cvxpy as cp
import numpy as np
from numpy.typing import ArrayLike
from itertools import combinations
from random import randint

def random_allocation(valuations: ArrayLike) -> np.ndarray:
    """Computes the probabilities of an envy free random allocation.
    
    >>> p = random_allocation([[3, 5], [5, 3]])
    >>> np.allclose([[0, 1], [1, 0]], p)
    True
    >>> p = random_allocation([[8, 15], [5, 23]])
    >>> np.allclose([[0.5, 0.5], [0.5, 0.5]], p)
    True
    

    Args:
        valuations (ArrayLike): Agents valuations of the items

    Returns:
        np.ndarray: The probablities matrix
    """
    valuations = np.asarray(valuations)

    probabilities = cp.Variable(valuations.shape)
    expected_utils = cp.multiply(valuations, probabilities).sum(axis=1)

    constraints = [
        probabilities >= 0,
        probabilities <= 1,
        probabilities.sum(axis=1) == 1,
        probabilities.sum(axis=0) == 1,
    ]
    
    for i, j in combinations(range(valuations.shape[0]), 2):
        vi_xj = cp.multiply(probabilities[j], valuations[i]).sum()
        vj_xi = cp.multiply(probabilities[i], valuations[j]).sum()
        constraints.append(expected_utils[i] >= vi_xj)
        constraints.append(expected_utils[j] >= vj_xi)

    objective = cp.Maximize(cp.sum(expected_utils))
    problem = cp.Problem(objective=objective, constraints=constraints)
    problem.solve()

    return probabilities.value
    

if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
    
