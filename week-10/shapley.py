import logging
import random

logger = logging.Logger(__name__)


def values(all_players: str, map_subset_to_cost: dict, num_perm: int):

    perm = list(all_players)
    res = {}
    for _ in range(num_perm):
        random.shuffle(perm)  # random permutation
        logger.debug("current permutation: %s.", perm)

        curr_cost = 0
        subset = []
        for player in perm:
            subset.append(player)
            subset.sort()
            new_cost = map_subset_to_cost["".join(subset)]
            marginal_cost = new_cost - curr_cost
            res[player] = res.get(player, 0) + marginal_cost
            logger.debug("Player %s marginal cost: %s.", player, marginal_cost)
            curr_cost = new_cost
    # Calculate mean
    for p, c in res.items():
        res[p] = c / num_perm
    return res


def research():
    tol = 1e-2
    players = list("abc")
    map_subset_to_cost = {
        "": 0,
        "a": 10,
        "b": 15,
        "c": 25,
        "ab": 20,
        "ac": 25,
        "bc": 30,
        "abc": 37,
    }
    shapley_values = {"a": 6.5, "b": 11.5, "c": 19}
    perm_count = 0
    acc_sum = {p: 0 for p in players}
    # UNCOMMENT SEED TO REPRODUCE OUTCOME
    random.seed(605546)
    while True:
        random.shuffle(players)
        perm_count += 1
        curr_cost = 0
        subset = []
        # Update marginal costs
        for p in players:
            subset.append(p)
            subset.sort()
            new_cost = map_subset_to_cost["".join(subset)]
            marginal_cost = new_cost - curr_cost
            acc_sum[p] += marginal_cost
            curr_cost = new_cost

        close_enough = all(
            abs(acc_sum[p] / perm_count - shapley_values[p]) <= tol * shapley_values[p]
            for p in players
        )
        if close_enough:
            break
    print("Number of random permutations to be close enough:", perm_count)
    return perm_count


if __name__ == "__main__":
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    research()