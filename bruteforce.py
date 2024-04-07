import csv
import resource
import time


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

    start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    start_time = time.time()

    for i in range(1, 2**len(actions)):
        action_set = []
        for j, action_name in enumerate(actions):
            if (i >> j) & 1:
                action = actions[action_name]
                action_set.append(action)

        total_cost = sum(action['cost'] for action in action_set)
        total_profit = sum(((action['profit'] * action['cost']) / 100) for action in action_set)

        if total_cost <= budget and total_profit > best_profit:
            best_actions = action_set
            best_profit = total_profit

    end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    end_time = time.time()

    memory_usage = end_memory - start_memory
    execution_time = end_time - start_time

    return best_actions, best_profit, memory_usage, execution_time


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


if __name__ == "__main__":
    actions = read_csv("actiontest1.csv")
    budget = 500
    best_actions, best_profit, memory_usage, execution_time = possible_combinations(actions, budget)

    print("Actions chosen for an investment of", budget, "€:")
    for action_details in best_actions:
        action_name = None
        for key, value in actions.items():
            if value == action_details:
                action_name = key
                break

        if action_name is not None:
            print("Action:", action_name, "- Cost:", action_details['cost'],
                  "€ - Profit:", action_details['profit'], "%")

    print("Total profit after 2 years:", best_profit, "€")
    print("Memory usage:", memory_usage, "bytes")
    print("Execution time:", execution_time, "seconds")
