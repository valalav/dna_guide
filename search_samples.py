#!/usr/bin/env python3
import csv

# Search aadna.ru.csv for samples matching R-Y210364 or related
samples_found = []

with open("aadna.ru.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        haplogroup = row.get("Haplogroup", "")
        subethnos = row.get("Субэтнос", "")
        surname = row.get("Фамилия", "")

        # Check for any match with Y210364
        if "Y210364" in haplogroup:
            samples_found.append(
                {
                    "Surname": surname,
                    "Subethnos": subethnos,
                    "Haplogroup": haplogroup,
                    "Location": row.get("Lacation", ""),
                    "Kit": row.get("Kit Number", ""),
                }
            )

        # Check child branches
        if (
            "Y210365" in haplogroup
            or "Y210367" in haplogroup
            or "Y210361" in haplogroup
        ):
            samples_found.append(
                {
                    "Surname": surname,
                    "Subethnos": subethnos,
                    "Haplogroup": haplogroup,
                    "Location": row.get("Lacation", ""),
                    "Kit": row.get("Kit Number", ""),
                }
            )

if samples_found:
    print(f"✅ Found {len(samples_found)} samples in aadna.ru.csv:\n")
    for sample in samples_found:
        print(f"Фамилия: {sample['Surname']}")
        print(f"Субэтнос: {sample['Subethnos']}")
        print(f"Гаплогруппа: {sample['Haplogroup']}")
        print(f"Населённый пункт: {sample['Location']}")
        print(f"Kit: {sample['Kit']}")
        print("---")
else:
    print("❌ No samples found in aadna.ru.csv matching R-Y210364 or its subclades")
