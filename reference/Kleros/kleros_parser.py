import os
import re
import pandas as pd

# 2) Walk all .sol files
kleros_dir = "../../../kleros"
kleros_interaction_dir = "../../../kleros-interaction"

pattern = re.compile(r'\b(\w+)\s+(?:public\s+)?constant\s+(\w+)\s*=\s*((?:"(?:\\.|[^"\\])*"|[^;])*);', re.DOTALL)


rows = []
for root, _, files in os.walk(kleros_dir):
    for fname in files:
        if fname.endswith(".sol"):
            path = os.path.join(root, fname)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('//') or not line:
                        continue  # skip comments or empty lines
                    m = pattern.search(line)
                    if m:
                        rows.append({
                            "file": os.path.relpath(path, kleros_dir),
                            "type": m.group(1),
                            "name": m.group(2),
                            "value": m.group(3).strip()
                        })

for root, _, files in os.walk(kleros_interaction_dir):
    for fname in files:
        if fname.endswith(".sol"):
            path = os.path.join(root, fname)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('//') or not line:
                        continue  # skip comments or empty lines
                    m = pattern.search(line)
                    if m:
                        rows.append({
                            "file": os.path.relpath(path, kleros_interaction_dir),
                            "type": m.group(1),
                            "name": m.group(2),
                            "value": m.group(3).strip()
                        })


# 3) Display it to you
df = pd.DataFrame(rows)
# tools.display_dataframe_to_user("Kleros Public Constants", df)
df.to_csv('kleros_constants.csv', index=False)
print(df.to_string(index=False))
