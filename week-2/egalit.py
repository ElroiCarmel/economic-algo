"""
Implementation and testing of the egalitarion and leximin-egalitarian allocation.
Author: Elroi Carmel
Date: 11-25
"""

import cvxpy as cp
from numpy.typing import ArrayLike
import numpy as np
from itertools import combinations


def egalitarian(valuation: ArrayLike, leximin: bool = False) -> np.ndarray:
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
    
    Leximin usage examples:
    >>> np.allclose(egalitarian(val, leximin=True), [[0, 1], [1, 0]])
    True
    >>> val = [[4, 0, 0], [0, 3, 0], [5, 5, 10], [5, 5, 10]]
    >>> expected = [[1, 0, 0], [0, 1, 0], [0, 0, 0.5], [0, 0, 0.5]]
    >>> np.allclose(egalitarian(val, leximin=True), expected)
    True

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

    base_constraints = [
        allocation_matrix >= 0,
        allocation_matrix <= 1,
        allocation_matrix.sum(axis=0) == 1,
    ]

    objective = cp.Maximize(min_utility)
    problem = cp.Problem(
        objective=objective,
        constraints=base_constraints + [utilities >= min_utility],
    )

    problem.solve()

    if leximin:
        utility_sums = utilities
        for subset_size in range(2, n + 1):
            # Add previous min_utility as constant
            for u_sum in utility_sums:
                base_constraints.append(u_sum >= min_utility.value)

            # Construt new utility sums combinations for this level
            utility_sums = [
                cp.sum(cp.hstack(combo))  # more efficient summing in cvxpy
                for combo in combinations(utilities, subset_size)
            ]
            # Update to the next min_utility
            min_utility = cp.Variable()
            leximin_constraints = [u_sum >= min_utility for u_sum in utility_sums]
            problem = cp.Problem(
                objective=cp.Maximize(min_utility),
                constraints=base_constraints + leximin_constraints,
            )
            problem.solve()

    final_allocation = allocation_matrix.value.round(2)
    return final_allocation


def summary(alloc: np.ndarray) -> str:
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


def allocate(valuation: ArrayLike, leximin: bool = False) -> None:
    allocation = egalitarian(valuation, leximin)
    print(summary(allocation))


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
