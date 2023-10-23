import pandas as pd
import matplotlib.pyplot as plt

# Read progress updates from the file into a pandas DataFrame
progress_df = pd.read_csv("progress.txt", header=None, names=["Progress"])

# Split the progress column into 'x' and 'y' columns
progress_df["Satisfied"], progress_df["Total"] = progress_df["Progress"].str.split("/", 1).str
progress_df["Satisfied"] = progress_df["Satisfied"].astype(int)
progress_df["Total"] = progress_df["Total"].astype(int)

# Plot the progress using pyplot
plt.plot(progress_df.index, progress_df["Satisfied"])
plt.xlabel("Iteration")
plt.ylabel("Number of Satisfied Clauses")
plt.title("Progress Over Iterations")
plt.show()
