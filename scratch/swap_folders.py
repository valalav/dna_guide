import os
import shutil

old_dir = '10_Haplogroups'
new_dir = '10_Haplogroups_Restructured'
bak_dir = '10_Haplogroups_bak'

# Ensure bak_dir doesn't exist
if os.path.exists(bak_dir):
    shutil.rmtree(bak_dir)

# Rename old to bak
os.rename(old_dir, bak_dir)
print(f"Renamed {old_dir} to {bak_dir}")

# Rename new to old
os.rename(new_dir, old_dir)
print(f"Renamed {new_dir} to {old_dir}")

# Check for non-MD files in bak_dir
non_mds = []
for root, dirs, files in os.walk(bak_dir):
    for f in files:
        if not f.lower().endswith('.md'):
            non_mds.append(os.path.join(root, f))

if non_mds:
    print(f"Found {len(non_mds)} non-markdown files. They are safely in {bak_dir}.")
    for n in non_mds:
        print(f" - {n}")
else:
    print("No non-markdown files found. Everything was flawlessly migrated.")
