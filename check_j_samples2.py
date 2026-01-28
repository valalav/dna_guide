import pandas as pd

# Read the data
df = pd.read_csv("aadna_data.csv")

# Find J haplogroup samples
j_samples = df[df["Haplogroup"].str.contains("J", na=False)]

print(f"Total J haplogroup samples: {len(j_samples)}")
print()

# Show relevant columns
relevant_cols = ["Фамилия", "Субэтнос", "Haplogroup", "Lacation", "Country"]
print(j_samples[relevant_cols].head(30))
print()

# Check for P81 specifically
p81_samples = j_samples[j_samples["Haplogroup"].str.contains("P81", na=False)]
print(f"J-P81 specific samples: {len(p81_samples)}")
if len(p81_samples) > 0:
    print(p81_samples[relevant_cols])
