
from web3 import Web3
import pandas as pd
from collections import defaultdict
import json
import sys

# Alchemy provider URL
provider_url = "https://eth-mainnet.g.alchemy.com/v2/sRkdZi-Tky5ig1x9fUjZnogeQA5Sdwj3"
w3 = Web3(Web3.HTTPProvider(provider_url))

if not w3.is_connected():
    raise ConnectionError("Failed to connect to Ethereum")

# Contract address and ABI
contract_address = Web3.to_checksum_address("0x988b3A538b618C7A603e1C11Ab82Cd16dbE28069")

# Topics
draw_topic = "0x" + w3.keccak(text="Draw(address,uint256,uint256,uint256)").hex()
shift_topic = "0x" + w3.keccak(text="TokenAndETHShift(address,uint256,int256,int256)").hex()

# Define block range
start_block = 7300000
end_block = w3.eth.block_number
step = 100000

# Juror count: disputeID -> count
juror_counts = defaultdict(int)
eth_rewards = defaultdict(int)
appeals = defaultdict(int)
# Fetch and decode logs in chunks
if sys.argv[1] == "--fetch": 
    for block_start in range(start_block, end_block, step):
        block_end = min(block_start + step - 1, end_block)
        print(f"📦 Blocks {block_start} to {block_end}")

        try:
            draw_logs = w3.eth.get_logs({
                "fromBlock": block_start,
                "toBlock": block_end,
                "address": contract_address,
                "topics": [draw_topic]
            })
            for log in draw_logs:
                dispute_id = int(log["topics"][2].hex(), 16)
                juror_counts[dispute_id] += 1
                data_bytes = bytes(log["data"][2:])
                appeal = int.from_bytes(data_bytes[:32], byteorder="big") // (2**16)
                appeals[dispute_id] = max(appeals[dispute_id], appeal)
        except Exception as e:
            print(f"⚠️ Draw log error: {e}")

        try:
            shift_logs = w3.eth.get_logs({
                "fromBlock": block_start,
                "toBlock": block_end,
                "address": contract_address,
                "topics": [shift_topic]
            })
            for log in shift_logs:
                dispute_id = int(log["topics"][2].hex(), 16)
                data_bytes = bytes(log["data"])
                eth_amt = int.from_bytes(data_bytes[-32:], byteorder="big", signed=True)
                eth_rewards[dispute_id] += eth_amt
        except Exception as e:
            print(f"⚠️ ETH shift log error: {e}")
    
    with open("juror_counts.json", "w") as f:
        json.dump(juror_counts, f)
    with open("eth_rewards.json", "w") as f:
        json.dump(eth_rewards, f)
    with open("appeals.json", "w") as f:
        json.dump(appeals, f)
elif sys.argv[1] == "--no-fetch":
    with open("juror_counts.json", "r") as f:
        juror_counts = json.load(f)
    with open("eth_rewards.json", "r") as f:
        eth_rewards = json.load(f)
    with open("appeals.json", "r") as f:
        appeals = json.load(f)

# Combine results
rows = []
for dispute_id in sorted(set(juror_counts.keys()) | set(eth_rewards.keys())):
    arbitration_cost = eth_rewards.get(dispute_id, 0) / 1e18
    jurors = juror_counts.get(dispute_id, 0)
    cost_per_juror = round(arbitration_cost / jurors, 4)
    appeal_count = appeals.get(dispute_id, 0)
    cost_per_appeal = round(arbitration_cost / (appeal_count + 1), 4)
    rows.append({
        "disputeNumber": dispute_id,
        "arbitrationCost": arbitration_cost,
        "jurorCount": jurors,
        "costPerJuror": cost_per_juror,
        "appealCount": appeal_count,
        "costPerAppeal": cost_per_appeal
    })

df = pd.DataFrame(rows)
df.to_csv("kleros_dispute_stats.csv", index=False)
print("✅ Saved: kleros_dispute_stats.csv")
