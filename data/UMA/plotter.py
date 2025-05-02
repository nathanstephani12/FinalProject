import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

SAVE_DIR = "../../figures/UMA/"
df = pd.read_csv('uma_assertions.csv')

# Open file for regression output
with open("regression.txt", "w") as reg_out:

    token_counts = df["currencySymbol"].value_counts()
    plt.figure(figsize=(8, 5))
    token_counts.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("Number of Assertions by Token")
    plt.xlabel("Token")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}assertions_by_token.png")

    settled = df[df["isSettled"]]
    plt.figure(figsize=(8, 5))
    plt.hist(settled["timeToSettlement"] / 3600, bins=30, color="lightgreen", edgecolor="black")
    plt.title("Time to Settlement (in Hours)")
    plt.xlabel("Hours")
    plt.ylabel("Number of Assertions")
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}settlement_time_histogram.png")

    plt.figure(figsize=(8, 5))
    df.boxplot(column="bondUSD", by="currencySymbol")
    plt.title("Bond Amounts by Token (USD)")
    plt.suptitle("")  # remove automatic boxplot title
    plt.xlabel("Token")
    plt.ylabel("Bond (USD)")
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}bond_by_token_boxplot.png")

    # --- Scatter Plot 1: Bond vs. Time to Settlement ---
    x1 = settled["bondUSD"]
    y1 = settled["timeToSettlement"] / 3600
    slope, intercept, r_value, _, _ = linregress(x1, y1)
    plt.figure(figsize=(8, 5))
    plt.scatter(x1, y1, alpha=0.6, c="dodgerblue", edgecolors="k", label="Data")
    plt.plot(x1, slope * x1 + intercept, color="red", label="Fit")
    plt.title("Bond Amount vs. Time to Settlement")
    plt.xlabel("Bond (USD)")
    plt.ylabel("Time to Settlement (Hours)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}bond_vs_settlement_time.png")

    reg_out.write("Bond vs. Time to Settlement:\n")
    reg_out.write(f"  Slope: {slope:.4f}\n  Intercept: {intercept:.4f}\n  R^2: {r_value**2:.4f}\n\n")

    # --- Scatter Plot 2: Bond vs. Time to Dispute ---
    disputed = df[df["wasDisputed"]]
    x2 = disputed["bondUSD"]
    y2 = disputed["timeToDispute"] / 3600
    slope, intercept, r_value, _, _ = linregress(x2, y2)
    plt.figure(figsize=(8, 5))
    plt.scatter(x2, y2, alpha=0.6, c="crimson", edgecolors="k", label="Data")
    plt.plot(x2, slope * x2 + intercept, color="black", label="Fit")
    plt.title("Bond Amount vs. Time to Dispute")
    plt.xlabel("Bond (USD)")
    plt.ylabel("Time to Dispute (Hours)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}bond_vs_dispute_time.png")

    reg_out.write("Bond vs. Time to Dispute:\n")
    reg_out.write(f"  Slope: {slope:.4f}\n  Intercept: {intercept:.4f}\n  R^2: {r_value**2:.4f}\n\n")

    # --- Scatter Plot 3: Bond vs. Asserter Win ---
    x3 = df["bondUSD"]
    y3 = df["asserterWon"].astype(int)
    plt.figure(figsize=(8, 5))
    plt.scatter(x3, y3, alpha=0.4, c="purple", edgecolors="gray", label="Data")
    plt.plot(x3, slope * x3 + intercept, color="green", label="Fit")
    plt.title("Bond Amount vs. Asserter Win")
    plt.xlabel("Bond (USD)")
    plt.ylabel("Asserter Won (1 = Yes)")
    plt.yticks([0, 1])
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}bond_vs_asserter_win.png")

