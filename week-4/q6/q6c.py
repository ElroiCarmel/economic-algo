import logging
import networkx as nx
import cvxpy as cp
from itertools import combinations

logging.basicConfig(level=logging.DEBUG, format="{levelname} - {message}", style="{")


def summary(valuations: list[list[float]], rooms_alloc: dict, pricing: dict) -> str:
    sentences = []
    for player in range(len(valuations)):
        room = rooms_alloc[player]
        val = valuations[player][room]
        price = round(pricing[player], 2)
        sentences.append(
            f"Player {player} gets room {room} with value {val}, and pays {price}"
        )
    return "\n".join(sentences)


def allocate_rooms(valuations: list[list[float]]) -> dict:
    g = nx.Graph()
    n, m = len(valuations), len(valuations[0])
    for i in range(n):
        for j in range(m):
            g.add_edge(
                f"player {i}", f"room {j}", weight=valuations[i][j], player=i, room=j
            )
    # Find the maximum allocation
    allocation_edges = nx.max_weight_matching(g)
    logging.debug("Max weighted matching: %s", allocation_edges)
    # Extract the allocation
    rooms_allocation = {}
    for u, v in allocation_edges:
        edge = g[u][v]
        rooms_allocation[edge["player"]] = edge["room"]
    return rooms_allocation


def envy_free_room_allocation(valuations: list[list[float]], rent: float) -> None:
    """Allocates room to players and give prices to the rooms.
    
    Usage example:
    >>> v, r = [[150, 10], [140, 10]], 130
    >>> envy_free_room_allocation(v, r)
    Pricing such that all prices > 0 doesn't exist
    >>> v, r = [[150, 10], [140, 10]], 150
    >>> envy_free_room_allocation(v, r)
    Player 0 gets room 0 with value 150, and pays 140.0
    Player 1 gets room 1 with value 10, and pays 10.0

    Args:
        valuations (list[list[float]]): The players valuations of the rooms
        rent (float): Total rent that needs to be paid
    """
    # 1. Rooms allocation
    rooms_allocation = allocate_rooms(valuations)
    logging.debug("Allocation dictionary: %s", rooms_allocation)

    # Linear programming for pricing
    num_players, num_rooms = len(valuations), len(valuations[0])
    prices = cp.Variable(num_rooms)
    # Dummy variable to simulate the " > 0 " constraint
    z = cp.Variable()  # minimum price
    constraints = [cp.sum(prices) == rent, prices >= z]
    # Add envy freenes
    for i, j in combinations(range(num_players), 2):
        xi, xj = rooms_allocation[i], rooms_allocation[j]
        vi_xj, vi_xi = valuations[i][xj], valuations[i][xi]
        vj_xi, vj_xj = valuations[j][xi], valuations[j][xj]
        constraints.append(vi_xi - prices[i] >= vi_xj - prices[j])
        constraints.append(vj_xj - prices[j] >= vj_xi - prices[i])
    # Maximize the minimum price
    problem = cp.Problem(objective=cp.Maximize(z), constraints=constraints)
    problem.solve()
    logging.debug("Status: %s", problem.status)
    logging.debug("Z Optimal value: %s", z.value.item())
    if z.value > 0:
        print(summary(valuations, rooms_allocation, prices.value.tolist()))
    else:
        print("Pricing such that all prices > 0 doesn't exist")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
    v = [[150, 0], [140, 10]]
    envy_free_room_allocation(valuations=v, rent=150)
