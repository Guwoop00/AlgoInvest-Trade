import csv
import time
from typing import List, Dict


MAX_BUDGET: int = 500


def find_best_action(shares_list: List[Dict[str, int]]) -> List[Dict[str, int]]:
    """
    Find the best combination of shares to invest in.

    Args:
        shares_list (list): A list of dictionaries containing information about available shares.
                            Each dictionary should have keys 'Action', 'Cost', and 'Profit'.

    Returns:
        list: A list of dictionaries representing the best combination of shares to invest in.
              Each dictionary contains keys 'Action', 'Cost', and 'Profit'.
    """
    budget: int = int(MAX_BUDGET * 100)
    shares_total: int = len(shares_list)
    cost: List[int] = []
    profit: List[int] = []

    for share in shares_list:
        cost.append(share["Cost"])
        profit.append(share["Profit"])

    dp: List[List[int]] = [
        [0 for _ in range(budget + 1)] for _ in range(shares_total + 1)
    ]

    for i in range(1, shares_total + 1):
        for j in range(1, budget + 1):
            if cost[i - 1] <= j:
                dp[i][j] = max(profit[i - 1] + dp[i - 1][j - cost[i - 1]], dp[i - 1][j])
            else:
                dp[i][j] = dp[i - 1][j]

    best_profit: List[Dict[str, int]] = []
    while budget >= 0 and shares_total >= 0:
        if (
            dp[shares_total][budget]
            == dp[shares_total - 1][budget - cost[shares_total - 1]]
            + profit[shares_total - 1]
        ):
            best_profit.append(shares_list[shares_total - 1])
            budget -= cost[shares_total - 1]
        shares_total -= 1

    return best_profit


def display_results(best_profit: List[Dict[str, int]]) -> None:
    """
    Display the results of the investment.

    Args:
        best_profit (list): A list of dictionaries representing the best combination of shares to invest in.
                            Each dictionary should have keys 'Action', 'Cost', and 'Profit'.

    Returns:
        None
    """
    print(f"\nMost profitable investment ({len(best_profit)} shares):\n")
    cost: List[float] = []
    profit: List[float] = []

    for item in best_profit:
        print(f"{item['Action']} {item['Cost'] / 100} € +{item['Profit'] / 100} €")
        cost.append(item["Cost"] / 100)
        profit.append(item["Profit"])

    print("\nTotal cost:", sum(cost), "€")
    print("Profit after 2 years: +", sum(profit) / 100, "€")


def read_csv(filename: str) -> List[Dict[str, int]]:
    """
    Read data from a CSV file and return a list of dictionaries containing information about available shares.

    Args:
        filename (str): The name of the CSV file.

    Returns:
        list: A list of dictionaries containing information about available shares.
              Each dictionary should have keys 'Action', 'Cost', and 'Profit'.
    """
    actions: List[Dict[str, int]] = []

    try:
        with open(filename, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if float(row["Cost"]) > 0 and float(row["Profit"]) > 0:
                    cost: int = int(float(row["Cost"]) * 100)
                    profit: int = int(float(row["Profit"]) * cost / 100)
                    actions.append(
                        {"Action": row["Share"], "Cost": cost, "Profit": profit}
                    )
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading CSV file '{filename}': {e}")

    return actions


# Launch
if __name__ == "__main__":

    start_time = time.time()

    actions: List[Dict[str, int]] = read_csv("actions.csv")
    best_profit: List[Dict[str, int]] = find_best_action(actions)
    display_results(best_profit)

    end_time = time.time()

    execution_time: float = end_time - start_time
    print("\nTime elapsed:", execution_time, "seconds")
