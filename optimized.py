import csv
import time

MAX_BUDGET = 500


def find_best_action(shares_list):
    budget = int(MAX_BUDGET * 100)
    shares_total = len(shares_list)
    cost = []
    profit = []

    for share in shares_list:
        cost.append(share['Cost'])
        profit.append(share['Profit'])

    dp = [[0 for _ in range(budget + 1)] for _ in range(shares_total + 1)]

    for i in range(1, shares_total + 1):
        for j in range(1, budget + 1):
            if cost[i - 1] <= j:
                dp[i][j] = max(profit[i - 1] + dp[i - 1][j - cost[i - 1]], dp[i - 1][j])
            else:
                dp[i][j] = dp[i - 1][j]

    best_profit = []
    while budget >= 0 and shares_total >= 0:
        if dp[shares_total][budget] == dp[shares_total - 1][budget - cost[shares_total - 1]] + profit[shares_total - 1]:
            best_profit.append(shares_list[shares_total - 1])
            budget -= cost[shares_total - 1]
        shares_total -= 1

    return best_profit


def display_results(best_profit):
    print(f"\nMost profitable investment ({len(best_profit)} shares):\n")
    cost = []
    profit = []

    for item in best_profit:
        print(f"{item['Action']} {item['Cost'] / 100} € +{item['Profit'] / 100} €")
        cost.append(item['Cost'] / 100)
        profit.append(item['Profit'])

    print("\nTotal cost:", sum(cost), "€")
    print("Profit after 2 years: +", sum(profit) / 100, "€")


def read_csv(filename):
    actions = []

    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if float(row['Cost']) > 0 and float(row['Profit']) > 0:
                    cost = int(float(row['Cost']) * 100)
                    profit = float(row['Profit']) * cost / 100
                    actions.append({'Action': row['Share'], 'Cost': cost, 'Profit': profit})
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading CSV file '{filename}': {e}")

    return actions


# Lunch
if __name__ == "__main__":

    start_time = time.time()

    actions = read_csv("actions.csv")
    best_profit = find_best_action(actions)
    display_results(best_profit)

    end_time = time.time()

    execution_time = end_time - start_time
    print("\nTime elapsed:", execution_time, "seconds")
