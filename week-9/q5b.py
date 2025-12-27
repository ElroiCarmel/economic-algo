import logging
from q5a import compute_medians

logger = logging.Logger(__name__)


def compute_breakpoints(
    total_budget: float, subjects_votes: list[list[float]]
) -> set[float]:
    num_phantoms = len(subjects_votes[0]) - 1
    res = {0, 1}
    for s in subjects_votes:
        for v in s:
            for i in range(1, num_phantoms + 1):
                res.add(1 / i)
                res.add(v / (total_budget * i))
    return res


def compute_budget(
    total_budget: float, citizen_votes: list[list[float]]
) -> list[float]:
    """
    Compute the budget for different. projects given the citizens preferences.

    In this implementaion we are first searching in the discrete space, then computing
    the exact 't' that for him sum of medians equal to total budget.

    Usage Example:
    >>> compute_budget(100, [[100, 0, 0], [0, 0, 100]])
    [50.0, 0, 50.0]
    """
    subjects_votes = list(map(list, zip(*citizen_votes)))
    breakpoints = sorted(compute_breakpoints(total_budget, subjects_votes))
    logger.debug("Breakpoints of t: %s.", breakpoints)
    # find the lower and upper tight bount for t
    t_lower_bound, t_upper_bound = 0, 1
    l, r = 0, len(breakpoints) - 1
    while l <= r:
        logger.debug("current search range: [%s, %s].", t_lower_bound, t_upper_bound)
        mid_idx = int((l + r) / 2)
        curr_t = breakpoints[mid_idx]
        logger.debug("checking for t=%s.", curr_t)
        medians = compute_medians(total_budget, subjects_votes, curr_t)
        logger.debug("medians of subjects votes: %s.", medians)
        total_sum = sum(medians)
        logger.debug("total sum: %s.", total_sum)
        if total_sum == total_budget:
            return medians
        elif total_sum < total_budget:
            t_lower_bound = curr_t
            lower_sum = total_sum
            l = mid_idx + 1
        else:
            t_upper_bound = curr_t
            upper_sum = total_sum
            r = mid_idx - 1
    logger.debug("the bounds for t are: [%s, %s].", t_lower_bound, t_upper_bound)
    logger.debug("the bouns of the total sum: [%s, %s].", lower_sum, upper_sum)
    # In these bounds the function for a given t is linear
    slope = (upper_sum - lower_sum) / (t_upper_bound - t_lower_bound)
    bias = upper_sum - t_upper_bound * slope
    t = (total_budget - bias) / slope

    logger.debug(
        "for t=%s, the sum of medians should be %s (total budget).", t, total_budget
    )
    medians = compute_medians(total_budget, subjects_votes, t)
    return medians


if __name__ == "__main__":
    import doctest

    # logger.addHandler(logging.StreamHandler())
    # logger.setLevel(logging.DEBUG)
    # budget = 100
    # cv = [[24, 70, 6], [37, 20, 43]]
    # compute_budget(budget, cv)
    print(doctest.testmod())
