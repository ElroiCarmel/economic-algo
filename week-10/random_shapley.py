from collections.abc import Iterable
import logging
import random

logger = logging.Logger(__name__)


def values(all_players: Iterable, map_subset_to_cost: dict, num_perm: int, cost_by_max: bool = False):

    perm = list(all_players)
    res = {}
    for _ in range(num_perm):
        random.shuffle(perm)  # random permutation
        logger.debug("current permutation: %s.", perm)

        curr_cost = 0
        subset = []
        for player in perm:
            if not cost_by_max:
                subset.append(player)
                subset.sort()
                new_cost = map_subset_to_cost[tuple(subset)]
            else:
                new_cost = max(map_subset_to_cost[player], curr_cost)
            
            marginal_cost = new_cost - curr_cost
            res[player] = res.get(player, 0) + marginal_cost
            logger.debug("Player %s marginal cost: %s.", player, marginal_cost)
            curr_cost = new_cost

    # Calculate mean
    for p, c in res.items():
        res[p] = c / num_perm

    return res


def is_close(truth: dict, p: dict, tol: float = 0.01):
    return all(
        abs(p[player] - truth[player]) <= tol * truth[player] for player in truth
    )


def section_b():
    all_players = "abc"
    map_subset_to_cost = {
        ("",): 0,
        ("a",): 10,
        ("b",): 15,
        ("c",): 25,
        ("a","b"): 20,
        ("a","c"): 25,
        ("b","c"): 30,
        ("a","b","c"): 37,
    }
    num_perm = 500
    ground_truth = {"a": 6.5, "b": 11.5, "c": 19}
    by_random = values(all_players, map_subset_to_cost, num_perm)
    for p in ground_truth:
        print(f"Player: {p}. Shapley value: {ground_truth[p]}. Random: {by_random[p]}")
    close = is_close(ground_truth, by_random)
    print(f"is close for {num_perm} random permutation: {close}.")


def airport_efficient(map_player_to_cost: dict):
    players = sorted(map_player_to_cost, key=map_player_to_cost.__getitem__)
    n = len(players)
    res = {players[0]: map_player_to_cost[players[0]] / n}

    for i in range(1, n):
        marginal_cost = (
            map_player_to_cost[players[i]] - map_player_to_cost[players[i - 1]]
        )
        res[players[i]] = (marginal_cost) / (n - i) + res[players[i - 1]]

    return res

def section_c():
    
    num_players_range = range(10, 101, 10)

    num_perm_start = 10_000
    for num_players in num_players_range:
        logger.info("checking for %s players.", num_players)
        instance = {p: random.randint(10, 101) for p in range(num_players)}
        logger.debug("random problem instance: %s.", instance)
        shapley_values = airport_efficient(instance)
        for num_perm in range(num_perm_start, int(1e10) + 1, 10_000):
            logger.info("%s random permutations:", num_perm)
            random_result = values(instance, instance, num_perm, cost_by_max=True)
            isclose = is_close(shapley_values, random_result)
            if isclose:
                print(f"For {num_players}, the result of the random algorithm is close enough for {num_perm}.")
                num_perm_start = num_perm
                break
            else:
                logger.info("random result is not close enough")
            

if __name__ == "__main__":
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

    # res = values("ab", {("",): 0, ("a",): 10, ("b",): 5, ("a","b"): 15}, 4)
    # print(res)
    # section_b()
    airport = {"a": 3, "b": 23, "c": 123}
    # print(airport_efficient(airport))
    # print(values(airport, airport, 10000))
    section_c()

