from typing import Optional
import cvxpy as cp
import numpy as np
from numpy.typing import ArrayLike
from random import randint

from q5a import random_allocation
    
def find_pareto_dominates(valuations: ArrayLike, baseline_utils: ArrayLike) -> Optional[ArrayLike]:
    """
    For section 3 in the question. To prove that for more than 2 players the algorithm doesn't always find
    a pareto optimal random allocation.
    """
    valuations = np.asarray(valuations)
    
    probabilities = cp.Variable(valuations.shape)
    expected_utils = cp.multiply(valuations, probabilities).sum(axis=1)

    constraints = [
        probabilities >= 0,
        probabilities <= 1,
        probabilities.sum(axis=1) == 1,
        probabilities.sum(axis=0) == 1,
        expected_utils >= baseline_utils 
    ]
    # No envy freenes constraints
    objective = cp.Maximize(cp.sum(expected_utils))
    problem = cp.Problem(objective=objective, constraints=constraints)
    problem.solve()    
    curr_sum = expected_utils.value.sum()
    prev_sum = np.sum(baseline_utils)
    if curr_sum > prev_sum:
        return probabilities.value
    


if __name__ == "__main__":
    # seed = randint(0, 2**31)
    seed = 2102834986
    print("seed:", seed)
    rng = np.random.default_rng(seed)
    n = 3
    val = rng.integers(size=(n, n), low=1, high=21)
    print("Agents valuations:\n", val)
    print("Find envy free allocations")
    probablities = random_allocation(val)
    print("Random allocation:\n", probablities.round(2))
    print("Agents utils:")
    agents_utils = (val * probablities).sum(axis=1)
    print(agents_utils.round(2))
    print("Search for more efficient random allocation.")
    dominates = find_pareto_dominates(val, agents_utils)
    if dominates is not None:
        print("Found pareto dominates random allocation")
        print("New probabilities:\n", dominates.round(2))
        print("New utils:", (dominates * val).sum(axis=1).round(2))
    else:
        print("Did not find one.")
    
