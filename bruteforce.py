import csv
import time


def possible_combinations(actions, budget):
    """
    Finds the possible combinations of actions within the given budget.

    Args:
        actions (dict): A dictionary containing actions as keys and their details (cost and profit) as values.
        budget (float): The budget available for investment.
        start_time (float): The start time of the execution.

    Returns:
        tuple: A tuple containing the best combination of actions and the total profit generated.
    """
    best_actions = []
    best_profit = 0

    for i in range(1, 2**len(actions)):
        action_set = []
        total_cost = 0
        total_profit = 0

        for j, action_name in enumerate(actions):
            if (i >> j) & 1:
                action = actions[action_name]
                action_set.append(action)
                total_cost += action['cost']
                total_profit += action['profit'] * action['cost'] / 100

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
                action = row['Share']
                cost = float(row['Cost'])
                profit = float(row['Profit'])
                actions[action] = {'cost': cost, 'profit': profit}
    except FileNotFoundError:
        print(f"Error: The file '{filename}' could not be found.")
    except Exception as e:
        print(f"Error while reading CSV file '{filename}': {e}")
    return actions


if __name__ == "__main__":

    start_time = time.time()

    actions = read_csv("actions.csv")
    budget = 500
    best_actions, best_profit = possible_combinations(actions, budget)

    end_time = time.time()

    execution_time = end_time - start_time

    print("Actions chosen for an investment of", budget, "€:")
    for action_details in best_actions:
        action_name = next((key for key, value in actions.items() if value == action_details), None)
        if action_name is not None:
            print("Action:", action_name, "- Cost:", action_details['cost'],
                  "€ - Profit:", action_details['profit'], "%")

    print("Total profit after 2 years:", round(best_profit, 2), "€")
    print("Execution time:", execution_time, "seconds")
