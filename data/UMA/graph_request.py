
import pandas as pd
import requests
from datetime import datetime

# Replace with your actual API key
api_key = 'a0abfce2447bce5aa1b2dee15ab2934a'
subgraph_id = 'Bm3ytsa1YvcyFJahdfQQgscFQVCcMvoXujzkd3Cz6aof'
url = f"https://gateway.thegraph.com/api/{api_key}/subgraphs/id/{subgraph_id}"

# === Paginated Assertion Fetch ===
all_assertions = []
skip = 0
batch_size = 1000
has_more = True

while has_more:
    paginated_query = f"""
    {{
      assertions(first: {batch_size}, skip: {skip}, orderBy: assertionTimestamp, orderDirection: desc) {{
        id
        asserter
        assertionId
        disputer
        disputeHash
        currency
        bond
        assertionTimestamp
        disputeTimestamp
        expirationTime
        settlementTimestamp
        settlementResolution
      }}
    }}
    """

    response = requests.post(url, json={'query': paginated_query})
    response.raise_for_status()
    result = response.json()

    if "errors" in result:
        print("GraphQL error:", result["errors"])
        break

    batch = result["data"]["assertions"]
    print(f"Retrieved {len(batch)} assertions at skip={skip}")
    all_assertions.extend(batch)

    has_more = len(batch) == batch_size
    skip += batch_size

# Convert to DataFrame
df = pd.DataFrame(all_assertions)

# Convert timestamps
for col in ["assertionTimestamp", "disputeTimestamp", "expirationTime", "settlementTimestamp"]:
    df[col] = pd.to_datetime(pd.to_numeric(df[col], errors='coerce'), unit='s', errors='coerce')


# Convert bond to float
df["bond"] = pd.to_numeric(df["bond"], errors="coerce")

# Define token metadata
token_info = {
    '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2': {'symbol': 'WETH', 'decimals': 18, 'price': 1844.6993}, #All conversion prices recieved 5/2/2025
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48': {'symbol': 'USDC', 'decimals': 6, 'price': 0.9999},
    '0xc770eefad204b5180df6a14ee197d99d808ee52d': {'symbol': 'FOX', 'decimals': 18, 'price': 0.029},
    '0x0954906da0bf32d5479e25f46056d22f08464cab': {'symbol': 'INDEX', 'decimals': 18, 'price': 1.50},
}

# Function to convert bond to USD
def convert_bond_to_usd(row):
    info = token_info.get(row['currency'].lower())
    if info:
        bond_normalized = row['bond'] / (10 ** info['decimals'])
        return bond_normalized * info['price']
    return None

# Apply conversion to DataFrame
df['currencySymbol'] = df['currency'].apply(lambda x: token_info.get(x.lower(), {}).get('symbol', 'Unknown'))
df['bondUSD'] = df.apply(convert_bond_to_usd, axis=1)


# Derived fields
df["wasDisputed"] = df["disputer"].notnull()
df["isSettled"] = df["settlementTimestamp"].notnull()
df["timeToDispute"] = (df["disputeTimestamp"] - df["assertionTimestamp"]).dt.total_seconds()
df["timeToSettlement"] = (df["settlementTimestamp"] - df["assertionTimestamp"]).dt.total_seconds()
df.loc[~df["isSettled"], "timeToSettlement"] = None

df["asserterWon"] = df["settlementResolution"] == True
df["disputerWon"] = df["settlementResolution"] == False

# Save to CSV
df.to_csv("uma_assertions.csv", index=False)




