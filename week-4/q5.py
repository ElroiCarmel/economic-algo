import logging
from itertools import combinations
import networkx as nx

# logging.basicConfig(level=logging.DEBUG)

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
        e = g[u][v]
        rooms_allocation[e["player"]] = e["room"]
    return rooms_allocation

def envy_free_room_allocation(valuations: list[list[float]], rent: float) -> str:
    # 1. Rooms allocation
    rooms_allocation = allocate_rooms(valuations)
    logging.debug("Allocation dictionary: %s", rooms_allocation)
    
    # Pricing
    # Build the envy-graph
    envy_graph = nx.DiGraph()
    num_players = len(valuations)
    for i, j in combinations(range(num_players), 2):
        xi, xj = rooms_allocation[i], rooms_allocation[j]
        vi_xj, vi_xi = valuations[i][xj], valuations[i][xi]
        vj_xi, vj_xj = valuations[j][xi], valuations[j][xj]
        i_envy, j_envy = vi_xj - vi_xi, vj_xi - vj_xj
        envy_graph.add_edge(i, j, envy=i_envy)
        envy_graph.add_edge(j, i, envy=j_envy)
    logging.debug("envy graph: %s", envy_graph.edges(data=True))
    # For each node find the heaviest path
    lengths = nx.all_pairs_bellman_ford_path_length(
        envy_graph, weight=lambda u, v, data: -data["envy"]
    )
    pricing = {}
    total_grants = 0
    for player, dist in lengths:
        grant = max(-x for x in dist.values())
        logging.debug("for player %s the dist is %s", player, dist)
        logging.debug("For player %s the heaviest envy path total weight is %s.", player, grant)
        # player gets a "grant"
        pricing[player] = -grant
        total_grants += grant
    price_for_all = (total_grants + rent) / num_players
    for player in pricing:
        pricing[player] += price_for_all
    logging.debug("Final pricing: %s.", pricing)
    print(summary(valuations, rooms_allocation, pricing))
    
if __name__ == "__main__":
    v = [[150, 0], [140, 10]]
    envy_free_room_allocation(valuations=v, rent=130)
