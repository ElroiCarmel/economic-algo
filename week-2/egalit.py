import cvxpy as cp
from numpy.typing import ArrayLike
import numpy as np


def egalitarian(valuation: ArrayLike, leximin: bool = False) -> None:
    valuation = np.asarray(valuation)  # convertion needed for cvxpy compatability
    n, m = valuation.shape
    # matrix[i, j] = x -> means agent i gets x portion of resource j
    allocation_matrix = cp.Variable(shape=(n, m))
    min_utility = cp.Variable()
    
    utilities = cp.multiply(valuation, allocation_matrix).sum(
        axis=1
    )  # element-wise multiplication

    constraints = [
        allocation_matrix >= 0,
        allocation_matrix <= 1,
        allocation_matrix.sum(axis=0) == 1,
        utilities >= min_utility,
    ]

    objective = cp.Maximize(min_utility)
    prob = cp.Problem(objective=objective, constraints=constraints)

    prob.solve()
    
    # TODO: Lexmin
    if leximin:
        pass
    
    
    
    
    rounded = allocation_matrix.value.round(2)
    print(allocation_summary(rounded))
    return rounded
    


def allocation_summary(alloc: np.ndarray) -> str:
    agents_summaries = []
    for agent_idx in range(len(alloc)):
        prefix = f"Agent #{agent_idx} gets "
        portions_strs = []
        for resource_idx in range(len(alloc[0])):
            portions_strs.append(
                f"{alloc[agent_idx, resource_idx].item()} of resource #{resource_idx}"
            )
        agents_summaries.append(prefix + ", ".join(portions_strs) +".")
    return "\n".join(agents_summaries)


if __name__ == "__main__":
    import doctest

