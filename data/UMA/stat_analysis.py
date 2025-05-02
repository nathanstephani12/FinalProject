import pandas as pd

df = pd.read_csv('uma_assertions.csv')

# === Summary Statistics ===
settled = df[df["isSettled"]]
disputed = df[df["wasDisputed"]]
disputed_settled = df[df["wasDisputed"] & df["isSettled"]]

with open("summary.txt", "w") as f:
  f.write("UMA Dispute Statistics:\n")
  f.write("Averages:\n")
  f.write(f"  Total assertions: {len(df)}\n")
  f.write(f"  Disputed assertions: {df['wasDisputed'].sum()} ({df['wasDisputed'].mean():.2%})\n")
  
  f.write(f"  Average bond: {df['bondUSD'].mean():.4f}USD\n")
  f.write(f"  Average bond (undisputed only): {df[~df['wasDisputed']]['bondUSD'].mean():.4f} USD\n")
  f.write(f"  Average bond (disputed only): {df[df['wasDisputed']]['bondUSD'].mean():.4f} USD\n")

  f.write(f"  Average time to dispute (if disputed): {disputed['timeToDispute'].mean():.2f} sec\n")
  f.write(f"  Average time to settlement (if settled): {settled['timeToSettlement'].mean():.2f} sec\n")

  # Global win rates (all settled)
  f.write(f"  Asserter win rate (all settled): {settled['asserterWon'].mean():.2%}\n")
  f.write(f"  Disputer win rate (all settled): {settled['disputerWon'].mean():.2%}\n")

  # Win rates only for disputed + settled
  f.write(f"  Asserter win rate (disputed only): {disputed_settled['asserterWon'].mean():.2%}\n")
  f.write(f"  Disputer win rate (disputed only): {disputed_settled['disputerWon'].mean():.2%}\n")

  f.write("\nDistributions:\n")
  f.write("Currency Symbol Distribution:\n")
  currency_counts = df["currencySymbol"].value_counts()
  for symbol, count in currency_counts.items():
    f.write(f"  {symbol}: {count}\n")

  f.write("\nBond Distribution (Overall):\n")
  f.write(f"  Min bond: {df['bondUSD'].min():.4f} USD\n")
  f.write(f"  Max bond: {df['bondUSD'].max():.4f} USD\n")
  f.write(f"  Mean bond: {df['bondUSD'].mean():.4f} USD\n")
  f.write(f"  Std Dev: {df['bondUSD'].std():.4f} USD\n")
  f.write(f"  Median bond: {df['bondUSD'].median():.4f} USD\n")



  f.write("\nBond Distribution by Currency Symbol:\n")
  bond_stats = df.groupby("currencySymbol")["bondUSD"].agg(["min", "max", "mean", "std", "median"])

  for symbol, row in bond_stats.iterrows():
      f.write(f"  {symbol}:\n")
      f.write(f"    Min: {row['min']:.4f} USD\n")
      f.write(f"    Max: {row['max']:.4f} USD\n")
      f.write(f"    Mean: {row['mean']:.4f} USD\n")
      f.write(f"    Std: {row['std']:.4f} USD\n")
      f.write(f"    Median: {row['median']:.4f} USD\n")

    # Settlement Time Distribution (for settled assertions only)
  f.write("\nSettlement Time Distribution (Settled Only):\n")
  settled = df[df["isSettled"]]
  f.write(f"  Min time to settlement: {settled['timeToSettlement'].min():.2f} sec\n")
  f.write(f"  Max time to settlement: {settled['timeToSettlement'].max():.2f} sec\n")
  f.write(f"  Mean time to settlement: {settled['timeToSettlement'].mean():.2f} sec\n")
  f.write(f"  Std Dev: {settled['timeToSettlement'].std():.2f} sec\n")
  f.write(f"  Median time to settlement: {settled['timeToSettlement'].median():.2f} sec\n")

