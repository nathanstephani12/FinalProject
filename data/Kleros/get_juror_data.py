import csv
import json
import pandas as pd
from web3 import Web3

# --- Setup ---
provider_url = "https://eth-mainnet.g.alchemy.com/v2/sRkdZi-Tky5ig1x9fUjZnogeQA5Sdwj3"
kleros_address = "0x988B3A538b618C7A603e1C11Ab82Cd16dbE28069"
w3 = Web3(Web3.HTTPProvider(provider_url))

# Load ABI
with open("KlerosLiquid.json") as f:
    kleros_abi = json.load(f)

contract = w3.eth.contract(address=w3.to_checksum_address(kleros_address), abi=kleros_abi)

# Load dispute IDs
disputes = pd.read_csv("kleros_disputes.csv")
dispute_ids = disputes['disputeNumber'].tolist()

# Collect vote data
records = []

for dispute_id in dispute_ids:
    try:
        dispute_info = contract.functions.getDispute(dispute_id).call()
        votes_lengths = dispute_info[1]  # second field is votesLengths array

        for appeal, num_votes in enumerate(votes_lengths):
            for vote_id in range(num_votes):
                try:
                    juror, _, choice, voted = contract.functions.getVote(dispute_id, appeal, vote_id).call()
                    records.append({
                        "disputeId": dispute_id,
                        "appeal": appeal,
                        "voteId": vote_id,
                        "juror": juror,
                        "choice": choice,
                        "voted": voted
                    })
                except Exception as e:
                    if "InvalidFEOpcode" in str(e):
                        print(f"🛑 Stopping early: no initialized vote at vote {vote_id} in appeal {appeal} for dispute {dispute_id}")
                        break
                    else:
                        print(f"⚠️ Failed to fetch vote {vote_id} in appeal {appeal} for dispute {dispute_id}: {e}")


    except Exception as e:
        print(f"⚠️ Failed to fetch dispute {dispute_id}: {e}")

# Save to CSV
df = pd.DataFrame(records)
df.to_csv("kleros_juror_votes.csv", index=False)
print("✅ Saved juror votes to kleros_juror_votes.csv")
