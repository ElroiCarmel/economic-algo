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
        price = pricing[player]
        sentences.append(f"Player {player} gets room {room} with value {val}, and pays {price}")
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

def envy_free_room_allocation(valuations: list[list[float]], rent: float) -> str:
    # 1. Rooms allocation
    rooms_allocation = allocate_rooms(valuations)
    logging.debug("Allocation dictionary: %s", rooms_allocation)
    
    # Linear programming for pricing
    num_rooms = len(valuations[0])
    prices = cp.Variable(num_rooms)
    constraints = [cp.sum(prices) == rent, prices >= 0]
    # Add envy freenes
    num_players = len(valuations)
    for i , j in combinations(range(num_players), 2):
        xi, xj = rooms_allocation[i], rooms_allocation[j]
        vi_xj, vi_xi = valuations[i][xj], valuations[i][xi]
        vj_xi, vj_xj = valuations[j][xi], valuations[j][xj]
        constraints.append(vi_xi - prices[i] >= vi_xj - prices[j])
        constraints.append(vj_xj - prices[j] >= vj_xi - prices[i])
    problem = cp.Problem(objective=cp.Maximize(0), constraints=constraints)
    problem.solve()
    logging.debug("Status: %s", problem.status)
    
    if problem.status == "infeasible":
        print("Pricing such that all prices >= 0 doesn't exist")
    else:
        print(summary(valuations, rooms_allocation, prices))

if __name__ == "__main__":
    v = [[150, 0], [140, 10]]
    envy_free_room_allocation(valuations=v, rent=120)
