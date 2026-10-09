import os
import shutil

base_dir = r"c:\Users\Admin\Downloads\INTERNATO GO\site_obstetricia"
index_file = os.path.join(base_dir, "index.html")
backup_file = os.path.join(base_dir, "scratch", "index.html.bak")
comp_file = os.path.join(base_dir, "components", "modulo-5-dmg-preeclampsia.html")

shutil.copyfile(index_file, backup_file)
print("Backup created at", backup_file)

with open(index_file, "r", encoding="utf-8") as f:
    index_lines = f.readlines()

with open(comp_file, "r", encoding="utf-8") as f:
    comp_content = f.read().strip()

# Find start and end indices in index_lines
m5_start_idx = None
m6_start_idx = None

for i, line in enumerate(index_lines):
    if '<section id="modulo-5"' in line:
        # Check if preceding line is the comment
        if i > 0 and '<!-- ==================== M' in index_lines[i-1]:
            m5_start_idx = i - 1
        else:
            m5_start_idx = i
        break

for i, line in enumerate(index_lines):
    if '<section id="modulo-6"' in line:
        if i > 0 and '<!-- ==================== M' in index_lines[i-1]:
            m6_start_idx = i - 1
        else:
            m6_start_idx = i
        break

print(f"M5 start index: {m5_start_idx}, M6 start index: {m6_start_idx}")

# Slice and replace
prefix = index_lines[:m5_start_idx]
suffix = index_lines[m6_start_idx:]

new_index_content = "".join(prefix) + "    " + comp_content + "\n\n" + "".join(suffix)

with open(index_file, "w", encoding="utf-8") as f:
    f.write(new_index_content)

print(f"index.html successfully updated! Total lines: {len(new_index_content.splitlines())}")
