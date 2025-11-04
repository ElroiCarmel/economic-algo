"""
Implementation and testing of the egalitarion and leximin-egalitarian allocation.
Author: Elroi Carmel
Date: 11-25
"""

import cvxpy as cp
from numpy.typing import ArrayLike
import numpy as np
from itertools import combinations


def egalitarian(
    valuation: ArrayLike, leximin: bool = False, verbose: bool = False
) -> np.ndarray:
    """
    Finds an allocation that maxmimize the minimum value of agents given allocations.
    The leximin variant maximizes also all of the other minimum values.

    Usage examples:
    >>> val = [[81, 19, 1], [70, 1, 29]]
    >>> np.allclose(egalitarian(val), [[0.53, 1, 0], [0.47, 0, 1]])
    True
    >>> val = [[0, 100], [50, 0]]
    >>> (val * egalitarian(val)).sum(axis=1).min().item()
    50.0

    Args:
        valuation (ArrayLike): Evaluation matrix. valuation[i, j] = p -> agent i values all of resource j as p.
        leximin (bool, optional): Use leximin variation of the algorithm. Defaults to False.

    Returns:
        np.ndarray: A matrix such that [i, j] entry means agent i receives [i, j] portion of resource j.
    """
    valuation = np.asarray(valuation)  # convertion needed for cvxpy compatability
    n, m = valuation.shape
    # matrix[i, j] = x -> means agent i gets x portion of resource j
    allocation_matrix = cp.Variable(shape=(n, m))
    min_utility = cp.Variable()

    utilities = cp.multiply(valuation, allocation_matrix).sum(
        axis=1
    )  # element-wise multiplication

    fixed_constraints = [
        allocation_matrix >= 0,
        allocation_matrix <= 1,
        allocation_matrix.sum(axis=0) == 1,
    ]

    objective = cp.Maximize(min_utility)
    prob = cp.Problem(
        objective=objective,
        constraints=fixed_constraints + [utilities >= min_utility],
    )

    prob.solve()

    # TODO: Lexmin
    if leximin:
        fixed_constraints.append(utilities >= min_utility.value)
        for c in range(2, n + 1):
            z = cp.Variable()
            cached = [cp.sum(cp.hstack(comb)) for comb in combinations(utilities, c)]
            temp = [cach >= z for cach in cached]
            prob = cp.Problem(objective=cp.Maximize(z), constraints=fixed_constraints + temp)
            prob.solve()
            for cach in cached:
                fixed_constraints.append(cach >= z.value)

    rounded = allocation_matrix.value.round(2)
    if verbose:
        print(allocation_summary(rounded))
    return rounded


def allocation_summary(alloc: np.ndarray) -> str:
    agents_summaries = []
    for agent_idx in range(len(alloc)):
        prefix = f"Agent #{agent_idx+1} gets "
        portions_strs = []
        for resource_idx in range(len(alloc[0])):
            portions_strs.append(
                f"{alloc[agent_idx, resource_idx].item()} of resource #{resource_idx+1}"
            )
        agents_summaries.append(prefix + ", ".join(portions_strs) + ".")
    return "\n".join(agents_summaries)


if __name__ == "__main__":
    import doctest

    # val = [[81, 19, 1], [70, 1, 29]]
    val = [[0, 100], [50, 0]]
    egalitarian(val, leximin=True, verbose=True)
    # print(doctest.testmod())
