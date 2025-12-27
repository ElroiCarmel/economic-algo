def elect_next_budget_item(
    votes: list[set[str]],
    balances: list[float],
    costs: dict[str, float],
) -> None:
    amount_of_supporters = dict()
    supporters_balance = dict()
    for voter, vote in enumerate(votes):
        voter_balance = balances[voter]
        for item in vote:
            supporters_balance[item] = supporters_balance.get(item, 0) + voter_balance
            amount_of_supporters[item] = amount_of_supporters.get(item, 0) + 1

    min_cost = float("inf")
    for item in costs:
        money_needed = (costs[item] - supporters_balance[item]) / amount_of_supporters[
            item
        ]
        if money_needed < min_cost:
            min_cost = money_needed
            chosen_item = item

    print(f'After adding {min_cost} to each citizen "{chosen_item}" is chosen.')

    # Giving the money
    for player in range(len(balances)):
        balances[player] += min_cost
        if chosen_item in votes[player]:
            balances[player] = 0
        print(f"Citizen {player} has {balances[player]} remaining balance.")


if __name__ == "__main__":
    # Demonstration
    votes = [
        {"a", "b"},
        {"b", "c"},
        {"a", "c"},
        {"a"},
        {"a", "c"},
    ]
    balances = [0, 0, 0, 0, 0]
    costs = {"a": 1, "b": 1, "c": 1}
    elect_next_budget_item(votes=votes, balances=balances, costs=costs)
