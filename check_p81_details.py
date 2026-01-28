import pandas as pd

# Read the data
df = pd.read_csv("aadna_data.csv")

# Find J-P81 specific samples
p81_samples = df[df["Haplogroup"] == "J-P81"]

print(f"Total J-P81 samples: {len(p81_samples)}")
print()

# Show all columns for better understanding
print("All P81 samples with details:")
relevant_cols = [
    "Фамилия",
    "Субэтнос",
    "Haplogroup",
    "Lacation",
    "Country",
    "Гг1",
    "Гг2",
    "Гг3",
    "Гг4",
    "Гг5",
    "Yfull_tree",
    "Lab",
    "Kit Number",
]
print(p81_samples[relevant_cols])
