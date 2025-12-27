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
                res.add(v / (total_budget * i))
    return res


def compute_budget(
    total_budget: float, citizen_votes: list[list[float]]
) -> list[float]:
    subjects_votes = list(map(list, zip(*citizen_votes)))
    breakpoints = sorted(compute_breakpoints(total_budget, subjects_votes))
    logger.debug("Breakpoints of t: %s.", breakpoints)
    # find the lower and upper tight bount for t
    t_lower_bound_idx, t_upper_bound_idx= 0, len(breakpoints) - 1
    while t_lower_bound_idx < t_upper_bound_idx:
        mid_idx = int((t_lower_bound_idx + t_upper_bound_idx) / 2)
        curr_t = breakpoints[mid_idx]
        
    
    
    
    

if __name__ == "__main__":
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    budget = 100
    cv = [[24, 70, 6], [37, 20, 43]]
    compute_budget(budget, cv)
