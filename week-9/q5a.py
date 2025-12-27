import logging
import math

logger = logging.Logger(__name__)


def f(i, t, c):
    return c * min(1, i * t)


def all_f(k, t, c):
    return [f(i, t, c) for i in range(1, k + 1)]


def compute_medians(total_budget: float, subjects_votes: list[list[float]], t) -> float:
    res = []
    dummy_votes = all_f(len(subjects_votes[0]) - 1, t, total_budget)
    logger.debug("dummy_votes: %s.", dummy_votes)
    for sv in subjects_votes:
        temp_vote = dummy_votes + sv
        temp_vote.sort()
        logger.debug("temp_vote: %s.", temp_vote)
        median = temp_vote[int(len(temp_vote) / 2)]
        res.append(median)
    return res


def compute_budget(
    total_budget: float, citizen_votes: list[list[float]]
) -> list[float]:
    """Compute budget according to the medians algorithm.

    Args:
        total_budget (float): Total budget for the projects.
        citizen_votes (list[list[float]]): Votes of each citizen how exactly should be allocated.

    Returns:
        list[float]: The budget to each project.
        
    Usage Example:
    >>> compute_budget(100, [[100, 0, 0], [0, 0, 100]])
    [50.0, 0, 50.0]
    
    
    """
    # find t such that total allocation equals total_budget
    l, r = 0, 1
    subjects_votes = list(map(list, zip(*citizen_votes)))
    # More convenient matrix for the algorrithm. ordered first by subject and then by citizen.
    logger.debug("subjects_votes: %s.", subjects_votes)
    while True:
        mid = (l + r) / 2
        logger.debug("left: %s, right: %s.", l, r)
        medians = compute_medians(total_budget, subjects_votes, mid)
        logger.debug("medians: %s.", medians)
        cur_budget_sum = sum(medians)
        logger.debug("current sum of medians: %s.", cur_budget_sum)
        if math.isclose(cur_budget_sum, total_budget):
            return medians
        elif cur_budget_sum < total_budget:
            l = mid
        else:
            r = mid


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
    