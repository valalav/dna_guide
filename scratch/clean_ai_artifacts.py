import os
import re

target_dirs = ['10_Haplogroups', '10_Haplogroups_bak', 'drafts', 'ralph']

# Match broader patterns of AI introductory sentences
pattern = re.compile(r"^\s*(I'll analyze|I will analyze|Let me analyze).*$", re.IGNORECASE | re.MULTILINE)
pattern2 = re.compile(r"^\s*(Here is an analysis|I've analyzed|I have analyzed).*$", re.IGNORECASE | re.MULTILINE)

count = 0
for tdir in target_dirs:
    if not os.path.exists(tdir): continue
    for root, dirs, files in os.walk(tdir):
        for f in files:
            if f.lower().endswith('.md'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                new_content = re.sub(pattern, "", content)
                new_content = re.sub(pattern2, "", new_content)
                
                # Cleanup multiple empty lines
                new_content = re.sub(r'\n{3,}', '\n\n', new_content)
                if new_content.startswith('\n'):
                    new_content = new_content.lstrip()

                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    count += 1

print(f"Cleaned AI artifacts from {count} files.")
