import pandas as pd

# Read the data
df = pd.read_csv("aadna_data.csv")

print("Columns:", df.columns.tolist())
print(f"Total rows: {len(df)}")
print()

# Find J haplogroup samples
j_samples = df[df["Haplogroup"].str.contains("J", na=False)]
print(f"J haplogroup samples: {len(j_samples)}")
print()

if len(j_samples) > 0:
    print(j_samples[["Surname", "Subethnos", "Haplogroup", "Location"]].head(20))
