import pandas as pd
from statistics import mode, StatisticsError
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Load CSV
df = pd.read_csv("kleros_dispute_stats.csv")

# Drop non-statistical columns
df = df.drop(columns=["disputeNumber"])

with open("summary.txt", "w") as f:
    pass # Clear contents of file

# Calculate and save stats for each column
for col in df.columns:
    col_data = df[col].dropna()

    # Mean and median
    mean_val = round(col_data.mean(), 4)
    median_val = round(col_data.median(), 4)
    min = col_data.min()
    max = col_data.max()

    # Mode with fallback
    try:
        mode_val = mode(col_data)
    except StatisticsError:
        mode_val = "No unique mode"

    with open("summary.txt", "a") as f:
        f.write(f"Statistic for '{col}':\n")
        f.write(f"  Mean:   {mean_val}\n")
        f.write(f"  Median: {median_val}\n")
        f.write(f"  Mode:   {mode_val}\n")
        f.write(f"  Min:    {min}\n")
        f.write(f"  Max:    {max}\n\n")

x = df["appealCount"]
y = df["jurorCount"]

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Save regression stats
with open("summary.txt", "a") as f:
    f.write("Appeals vs Jurors:\n")
    f.write(f"    Slope: {slope:.4f}\n")
    f.write(f"    Intercept: {intercept:.2f}\n")
    f.write(f"    R-squared: {r_value**2:.4f}\n\n")

# Plot the data
plt.figure(figsize=(10, 6))
plt.scatter(x, y, alpha=0.6, edgecolors='k', label="Data")
plt.plot(x, intercept + slope * x, color="red", label="Fit Line")
plt.title("Juror Count by Appeal Count (Linear Regression)")
plt.xlabel("Appeal Count")
plt.ylabel("Juror Count")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("../../figures/Kleros/appeals_v_jurors.png")

x = df["appealCount"]
y = df["arbitrationCost"]

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Save regression stats
with open("summary.txt", "a") as f:
    f.write("Appeals vs Cost:\n")
    f.write(f"    Slope: {slope:.4f}\n")
    f.write(f"    Intercept: {intercept:.2f}\n")
    f.write(f"    R-squared: {r_value**2:.4f}\n\n")

# Plot the data
plt.figure(figsize=(10, 6))
plt.scatter(x, y, alpha=0.6, edgecolors='k', label="Data")
plt.plot(x, intercept + slope * x, color="red", label="Fit Line")
plt.title("Arbitration Cost by Appeal Count (Linear Regression)")
plt.xlabel("Appeal Count")
plt.ylabel("Arbitration Cost")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("../../figures/Kleros/appeals_v_cost.png")

x = df["jurorCount"]
y = df["arbitrationCost"]

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Save regression stats
with open("summary.txt", "a") as f:
    f.write("Jurors vs Cost:\n")
    f.write(f"    Slope: {slope:.4f}\n")
    f.write(f"    Intercept: {intercept:.2f}\n")
    f.write(f"    R-squared: {r_value**2:.4f}\n\n")

# Plot the data
plt.figure(figsize=(10, 6))
plt.scatter(x, y, alpha=0.6, edgecolors='k', label="Data")
plt.plot(x, intercept + slope * x, color="red", label="Fit Line")
plt.title("Arbitration Cost by Juror Count (Linear Regression)")
plt.xlabel("Juror Count")
plt.ylabel("Arbitration Cost")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("../../figures/Kleros/jurors_v_cost.png")