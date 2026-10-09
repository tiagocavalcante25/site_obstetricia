import os
import re

base_dir = r"c:\Users\Admin\Downloads\INTERNATO GO\site_obstetricia"
comp_path = os.path.join(base_dir, "components", "modulo-5-dmg-preeclampsia.html")

with open(comp_path, "r", encoding="utf-8") as f:
    content = f.read()

# Locate section 5.2 boundary
m5_has_start = content.find('<!-- 5.2 PREECLAMPSIA, ECLAMPSIA & HELLP -->')
if m5_has_start == -1:
    m5_has_start = content.find('id="modulo-5-has"')
    m5_has_start = content.rfind('<div', 0, m5_has_start)

print("Found m5_has_start at index:", m5_has_start)
