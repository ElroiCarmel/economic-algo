import random
import logging

logger = logging.Logger(__name__)


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


def research():
    tol = 1e-2
    logger.info("Relational tolerance: %s.", tol)
    num_players_range = range(10, 101, 10)
    for num_players in num_players_range:
        # UNCOMMENT SEED TO REPRODUCE OUTCOME
        random.seed(959295725)
        logger.info("checking for %s players.", num_players)
        instance = {p: random.randint(10, 101) for p in range(num_players)}
        players = list(instance)
        logger.debug("random problem instance: %s.", instance)
        shapley_values = airport_efficient(instance)
        logger.debug("true shapley values: %s.", shapley_values)
        perm_count = 0
        acc_sum = {p: 0 for p in players}
        while True:
            random.shuffle(players)
            perm_count += 1
            curr_cost = 0
            # Update marginal costs
            for p in players:
                new_cost = max(curr_cost, instance[p])
                marginal_cost = new_cost - curr_cost
                acc_sum[p] += marginal_cost
                curr_cost = new_cost

            close_enough = all(
                abs(acc_sum[p] / perm_count - shapley_values[p])
                <= tol * shapley_values[p]
                for p in players
            )
            if close_enough:
                break
            logger.debug("%s rand permuts are not enough.", perm_count)
        logger.info("Number of random permutations to be close enough: %s.", perm_count)


if __name__ == "__main__":
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    research()