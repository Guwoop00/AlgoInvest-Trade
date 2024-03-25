import csv


def possible_combinations(actions, budget):
    """
    Finds the possible combinations of actions within the given budget.

    Args:
        actions (dict): A dictionary containing actions as keys and their details (cost and profit) as values.
        budget (float): The budget available for investment.

    Returns:
        tuple: A tuple containing the best combination of actions and the total profit generated.
    """
    best_actions = []
    best_profit = 0

    for i in range(1, 2**len(actions)):
        action_set = [actions[action] for j, action in enumerate(actions) if (i >> j) & 1]
        total_cost = sum(action['cost'] for action in action_set)
        total_profit = sum(((action['profit'] * action['cost']) / 100) for action in action_set)

        if total_cost <= budget and total_profit > best_profit:
            best_actions = action_set
            best_profit = total_profit

    return best_actions, best_profit


def read_csv(filename):
    """
    Reads data from a CSV file and returns a dictionary.

    Args:
        filename (str): The name of the CSV file to read.

    Returns:
        dict: A dictionary containing the data read from the CSV file.
              Keys are action names and values are dictionaries with keys 'cost' and 'profit'.
    """
    actions = {}

    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                action = row['Action']
                cost = float(row['Coût'])
                profit = float(row['Bénéfice'])
                actions[action] = {'cost': cost, 'profit': profit}
    except FileNotFoundError:
        print(f"Error: The file '{filename}' could not be found.")
    except Exception as e:
        print(f"Error while reading CSV file '{filename}': {e}")
    return actions


# Example usage of read_csv function
actions = read_csv("actions.csv")
budget = 500
best_actions, best_profit = possible_combinations(actions, budget)

print("Actions chosen for an investment of", budget, "€:")
for action in best_actions:
    print("Action:", [key for key, value in actions.items() if value == action][0], "- Cost:", action['cost'], "€ - Profit:", action['profit'], "%")

print("Total profit after 2 years:", best_profit, "€")
