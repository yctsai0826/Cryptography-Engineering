import random
import numpy as np
from collections import Counter

# Define the Naive shuffle algorithm
def naive_shuffle(cards):
    for i in range(len(cards)):
        n = random.randint(0, len(cards) - 1)
        cards[i], cards[n] = cards[n], cards[i]
    return cards

# Define the Fisher-Yates (Knuth) shuffle algorithm
def fisher_yates_shuffle(cards):
    for i in range(len(cards) - 1, 0, -1):
        n = random.randint(0, i)
        cards[i], cards[n] = cards[n], cards[i]
    return cards

# Function to simulate the shuffles a million times and count the results
def simulate_shuffles(shuffle_func, times=1_000_000):
    cards = [1, 2, 3, 4]
    shuffle_results = Counter()
    for _ in range(times):
        shuffled_cards = shuffle_func(cards[:])  # Make a copy of the cards for shuffling
        shuffle_results[tuple(shuffled_cards)] += 1
    return shuffle_results

# Simulate both shuffles a million times each
naive_results = simulate_shuffles(naive_shuffle)
fisher_yates_results = simulate_shuffles(fisher_yates_shuffle)

# Let's create a function to format the results as requested
def format_results(results, per_line=4):
    formatted_result_lines = []
    results_list = list(results.items())
    for i in range(0, len(results_list), per_line):
        line = ", ".join(["{}: {}".format(list(k), v) for k, v in results_list[i:i+per_line]])
        formatted_result_lines.append(line)
    return "\n".join(formatted_result_lines)

# Using the previous results, let's format them
naive_formatted = format_results(naive_results)
fisher_yates_formatted = format_results(fisher_yates_results)

print("naive:")
print(naive_formatted)
print('')
print("fisher_yates")
print(fisher_yates_formatted)

# Calculate the standard deviation of the results
naive_values = np.array(list(naive_results.values()))
fisher_yates_values = np.array(list(fisher_yates_results.values()))

naive_std = np.std(naive_values)
fisher_yates_std = np.std(fisher_yates_values)

print('')
print(f'naive standard deviation: {naive_std}')
print(f'fisher-yates standard deviation: {fisher_yates_std}')
