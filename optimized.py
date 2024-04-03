import csv


def possible_combinations(actions, budget):
    """
    Finds the possible combinations of actions within the given budget.

    Args:
        actions (list): A list containing dictionaries with actions details (cost and profit).
        budget (float): The budget available for investment.

    Returns:
        tuple: A tuple containing the best combination of actions and the total profit generated.
    """
    dp = [None] * (int(budget) + 1)
    dp[0] = ([], 0)

    for action in actions:
        for j in range(int(budget), int(action['Coût']) - 1, -1):
            if dp[j - int(action['Coût'])] is not None:
                new_profit = dp[j - int(action['Coût'])][1] + action['Bénéfice'] * action['Coût'] / 100
                if dp[j] is None or new_profit > dp[j][1]:
                    new_actions = dp[j - int(action['Coût'])][0] + [action]
                    dp[j] = (new_actions, new_profit)

    return dp[int(budget)]


def read_csv(filename):
    """
    Reads data from a CSV file and returns a list of dictionaries.

    Args:
        filename (str): The name of the CSV file to read.

    Returns:
        list: A list containing dictionaries with the data read from the CSV file.
              Each dictionary represents an action with keys 'Coût' and 'Bénéfice'.
    """
    actions = []

    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['Action']
                cost = float(row['Coût'])
                profit = float(row['Bénéfice'])
                actions.append({'Action': name, 'Coût': cost, 'Bénéfice': profit})
    except FileNotFoundError:
        print(f"Error: The file '{filename}' could not be found.")
    except Exception as e:
        print(f"Error while reading CSV file '{filename}': {e}")
    return actions


# Lunch
actions = read_csv("actions.csv")
budget = 500
best_actions, best_profit = possible_combinations(actions, budget)

print("Actions chosen for an investment of", budget, "€:")
for action in best_actions:
    print(action['Action'], "Cost:", action['Coût'], "€ - Profit:", action['Bénéfice'], "%")

print("Total profit after 2 years:", best_profit, "€")
