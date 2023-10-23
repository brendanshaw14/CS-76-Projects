import pandas as pd
import matplotlib.pyplot as plt

# Read progress updates from the file into a pandas DataFrame
df = pd.read_csv('Sudoku/solutions/all_cells_progress.txt', sep='/', header=None, names=['Clauses Satisfied', 'Total Clauses'])


# Plot the progress using pyplot
plt.plot(df.index, df["Clauses Satisfied"])
plt.xlabel("Iteration")
plt.ylabel("Number of Satisfied Clauses")
plt.title("Progress Over Iterations")
plt.show()
