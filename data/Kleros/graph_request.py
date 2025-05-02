import pandas as pd
import os
import requests

# Replace with your actual API key
api_key = 'a0abfce2447bce5aa1b2dee15ab2934a'
subgraph_id = 'BqbBhB4R5pNAtdYya2kcojMrQMp8nVHioUnP22qN8JoN'
url = f"https://gateway.thegraph.com/api/{api_key}/subgraphs/id/{subgraph_id}"

# === Paginated Dispute Fetch ===
all_disputes = []
skip = 0
batch_size = 1000
has_more = True

while has_more:
    paginated_query = f"""
    {{
      disputes(first: {batch_size}, skip: {skip}, orderBy: disputeIDNumber, orderDirection: desc) {{
        id
        disputeIDNumber
        arbitrated
        metaEvidenceId
        ruled
        ruling
      }}
    }}
    """
    response = requests.post(url, json={'query': paginated_query})
    response.raise_for_status()
    result = response.json()

    if "errors" in result:
        print("GraphQL error:", result["errors"])
        break

    batch = result["data"]["disputes"]
    print(f"✅ Retrieved {len(batch)} disputes at skip={skip}")
    all_disputes.extend(batch)
    
    has_more = len(batch) == batch_size
    skip += batch_size

# Convert to DataFrame and save
disputes = pd.DataFrame(all_disputes)
disputes.rename(columns={
    "id": "disputeId",
    "disputeIDNumber": "disputeNumber",
    "arbitrated": "arbitratedAddress",
    "metaEvidenceId": "metaEvidenceId"
}, inplace=True)
disputes.to_csv("kleros_disputes.csv", index=False)
print("🔄 All disputes saved to kleros_disputes.csv")
print(f"✅ Total Disputes: {len(disputes)}")
print(f"✅ Resolved: {disputes['ruled'].sum()}")
print(f"✅ Unresolved: {(~disputes['ruled']).sum()}")

# === Arbitrable Histories (non-paginated) ===
query = """
{
  arbitrableHistories(first: 10) {
    id
    metaEvidence
    disputes {
      id
    }
  }
}
"""

response = requests.post(url, json={'query': query})
if response.ok:
    data = response.json()
    arbitrables = pd.json_normalize(data["data"]["arbitrableHistories"])
    arbitrables.rename(columns={
        "id": "arbitrableId",
        "metaEvidence": "metaEvidenceURI"
    }, inplace=True)
    arbitrables.to_csv("kleros_arbitrable_histories.csv", index=False)
    print("📄 Arbitrable histories saved to kleros_arbitrable_histories.csv")
else:
    print("⚠️ Failed to fetch arbitrableHistories")
