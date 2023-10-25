import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_walksat_all_cells():
    numerators = {}  # Use a dictionary to store numerators for each file
    denominators = []  # List to store denominators

    # Iterate through your files and extract numerators
    for i in range(1, 10):
        numerators["0." + str(i)] = []
        file_path = f"Sudoku/data/all_cells_walksat_0.{i}.txt"
        with open(file_path, 'r') as file:
            for line in file:
                numerator = int(line.strip().split('/')[0])  # Extract numerator before '/'
                numerators["0." + str(i)].append(numerator)
            print(len(numerators["0." + str(i)]))

    # Extract denominators from a specific file (e.g., 'all_cells_walksat_0.1.txt')
    file_path = f"Sudoku/data/all_cells_walksat_0.1.txt"
    with open(file_path, 'r') as file:
        for line in file:
            denominator = int(line.strip().split('/')[1])  # Extract denominator after '/'
            denominators.append(denominator)

    # Find the maximum length among all lists in numerators
    max_length = max(len(numerators[key]) for key in numerators)

    # Fill missing values in each list with NaN to match the maximum length
    for key in numerators:
        current_length = len(numerators[key])
        if current_length < max_length:
            num_missing_values = max_length - current_length
            numerators[key] += [np.nan] * num_missing_values
        print(len(numerators[key]))
    print(numerators)
    # Create a DataFrame from the dictionary of numerators
    all_cells_df = pd.DataFrame(numerators)

    # # Add a 'Denominators' column to the DataFrame
    all_cells_df['Goal'] = denominators

    print(all_cells_df)
    # Plot each column with its label
    for column in all_cells_df.columns:
        plt.plot(all_cells_df.index, all_cells_df[column], label=column)

    # Customize the plot (add labels, legend, etc. as needed)
    plt.xlabel('Iterations Used')
    plt.ylabel('Constraints Solved')
    plt.title('WalkSAT Threshold Value Performances: All Cells')
    plt.legend()
    plt.show()

def plot_gsat_all_cells():
    numerators = {}  # Use a dictionary to store numerators for each file
    denominators = []  # List to store denominators

    # Iterate through your files and extract numerators
    for i in range(3, 10):
        numerators["0." + str(i)] = []
        file_path = f"Sudoku/data/all_cells_gsat_0.{i}.txt"
        with open(file_path, 'r') as file:
            for line in file:
                numerator = int(line.strip().split('/')[0])  # Extract numerator before '/'
                numerators["0." + str(i)].append(numerator)
            print(len(numerators["0." + str(i)]))

    # Extract denominators from a specific file (e.g., 'all_cells_walksat_0.1.txt')
    file_path = f"Sudoku/data/all_cells_gsat_0.3.txt"
    with open(file_path, 'r') as file:
        for line in file:
            denominator = int(line.strip().split('/')[1])  # Extract denominator after '/'
            denominators.append(denominator)

    # Find the maximum length among all lists in numerators
    max_length = max(len(numerators[key]) for key in numerators)

    # Fill missing values in each list with NaN to match the maximum length
    for key in numerators:
        current_length = len(numerators[key])
        if current_length < max_length:
            num_missing_values = max_length - current_length
            numerators[key] += [np.nan] * num_missing_values

    # Create a DataFrame from the dictionary of numerators
    all_cells_df = pd.DataFrame(numerators)

    # # Add a 'Denominators' column to the DataFrame
    all_cells_df['Goal'] = denominators

    print(all_cells_df)
    # Plot each column with its label
    for column in all_cells_df.columns:
        plt.plot(all_cells_df.index, all_cells_df[column], label=column)

    # Customize the plot (add labels, legend, etc. as needed)
    plt.xlabel('Iterations Used')
    plt.ylabel('Constraints Solved')
    plt.title('GSAT Threshold Value Performances: All Cells')
    plt.legend()
    plt.show()

def plot_gsat_rules():
    numerators = {}  # Use a dictionary to store numerators for each file
    denominators = []  # List to store denominators

    # Iterate through your files and extract numerators
    for i in range(1, 9):
        numerators["0." + str(i)] = []
        file_path = f"Sudoku/data/rules.cnf_gsat_0.{i}.txt"
        with open(file_path, 'r') as file:
            for line in file:
                numerator = int(line.strip().split('/')[0])  # Extract numerator before '/'
                numerators["0." + str(i)].append(numerator)
            print(len(numerators["0." + str(i)]))

    # Extract denominators from a specific file (e.g., 'all_cells_walksat_0.1.txt')
    file_path = f"Sudoku/data/rules.cnf_gsat_0.1.txt"
    with open(file_path, 'r') as file:
        for line in file:
            denominator = int(line.strip().split('/')[1])  # Extract denominator after '/'
            denominators.append(denominator)

    # Find the maximum length among all lists in numerators
    max_length = max(len(numerators[key]) for key in numerators)

    # Fill missing values in each list with NaN to match the maximum length
    for key in numerators:
        current_length = len(numerators[key])
        if current_length < max_length:
            num_missing_values = max_length - current_length
            numerators[key] += [np.nan] * num_missing_values

    # Create a DataFrame from the dictionary of numerators
    all_cells_df = pd.DataFrame(numerators)

    # # Add a 'Denominators' column to the DataFrame
    all_cells_df['Goal'] = denominators

    print(all_cells_df)
    # Plot each column with its label
    for column in all_cells_df.columns:
        plt.plot(all_cells_df.index, all_cells_df[column], label=column)

    # Customize the plot (add labels, legend, etc. as needed)
    plt.xlabel('Iterations Used')
    plt.ylabel('Constraints Solved')
    plt.title('GSAT Threshold Value Performances: All Rules')
    plt.legend()
    plt.show()

def plot_walksat_rules():
    numerators = {}  # Use a dictionary to store numerators for each file
    denominators = []  # List to store denominators

    # Iterate through your files and extract numerators
    for i in range(1, 10):
        numerators["0." + str(i)] = []
        file_path = f"Sudoku/data/rules.cnf_walksat_0.{i}.txt"
        with open(file_path, 'r') as file:
            for line in file:
                numerator = int(line.strip().split('/')[0])  # Extract numerator before '/'
                numerators["0." + str(i)].append(numerator)
            print(len(numerators["0." + str(i)]))

    # Extract denominators from a specific file (e.g., 'all_cells_walksat_0.1.txt')
    file_path = f"Sudoku/data/rules.cnf_walksat_0.1.txt"
    with open(file_path, 'r') as file:
        for line in file:
            denominator = int(line.strip().split('/')[1])  # Extract denominator after '/'
            denominators.append(denominator)

    # Find the maximum length among all lists in numerators
    max_length = max(len(numerators[key]) for key in numerators)

    # Fill missing values in each list with NaN to match the maximum length
    for key in numerators:
        current_length = len(numerators[key])
        if current_length < max_length:
            num_missing_values = max_length - current_length
            numerators[key] += [np.nan] * num_missing_values

    # Create a DataFrame from the dictionary of numerators
    all_cells_df = pd.DataFrame(numerators)

    # # Add a 'Denominators' column to the DataFrame
    all_cells_df['Goal'] = denominators

    print(all_cells_df)
    # Plot each column with its label
    for column in all_cells_df.columns:
        plt.plot(all_cells_df.index, all_cells_df[column], label=column)

    # Customize the plot (add labels, legend, etc. as needed)
    plt.xlabel('Iterations Used')
    plt.ylabel('Constraints Solved')
    plt.ylim(3200, 3260)
    plt.title('WalkSAT Threshold Value Performances: All Rules')
    plt.legend()
    plt.show()

plot_walksat_rules()
