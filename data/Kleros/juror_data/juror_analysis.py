import pandas as pd

# Load the dataset
df = pd.read_csv("kleros_juror_votes.csv")

# Filter out invalid choices (keep only 0, 1, 2)
df_valid = df[df['choice'].isin([0, 1, 2])]

# 1. Juror-level behavior
juror_stats = df.groupby('juror').agg(
    total_votes=('voteId', 'count'),
    votes_cast=('voted', lambda x: (x == True).sum()),
    votes_missed=('voted', lambda x: (x == False).sum()),
    vote_0=('choice', lambda x: (x == 0).sum()),
    vote_1=('choice', lambda x: (x == 1).sum()),
    vote_2=('choice', lambda x: (x == 2).sum())
)
juror_stats['participation_rate'] = juror_stats['votes_cast'] / juror_stats['total_votes']

# 2. Anomalies (unexpected vote values)
invalid_votes = df[~df['choice'].isin([0, 1, 2])]

# 3. Voting participation per dispute
dispute_participation = df.groupby('disputeId').agg(
    total_jurors=('juror', 'count'),
    votes_cast=('voted', lambda x: (x == True).sum()),
    votes_missed=('voted', lambda x: (x == False).sum())
)

# Save results to CSV
juror_stats.to_csv("juror_stats.csv")
invalid_votes.to_csv("invalid_votes.csv", index=False)
dispute_participation.to_csv("dispute_participation.csv")

with open("juror_summary.txt", "w") as f:
    f.write(f"Average votes per juror: {juror_stats['votes_cast'].mean()}\n")
    f.write(f"Median votes per juror: {juror_stats['votes_cast'].median()}\n")
    f.write(f"Average participation rate: {juror_stats['participation_rate'].mean()}\n")
    f.write(f"Median participation rate: {juror_stats['participation_rate'].median()}\n")


print("Analysis complete. Output saved")
