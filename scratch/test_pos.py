import os
import re

base_dir = r"c:\Users\Admin\Downloads\INTERNATO GO\site_obstetricia"
comp_file = os.path.join(base_dir, "components", "modulo-5-dmg-preeclampsia.html")

with open(comp_file, "r", encoding="utf-8") as f:
    orig_content = f.read()

# Locate section 5.1 and 5.2 boundary
# We want to replace from '<!-- 5.2 PREECLAMPSIA, ECLAMPSIA & HELLP -->' to the end of modulo-5-content
pos_52 = orig_content.find('<!-- 5.2 PREECLAMPSIA, ECLAMPSIA & HELLP -->')
if pos_52 == -1:
    pos_52 = orig_content.find('<div id="modulo-5-has"')

print("Index of 5.2 start:", pos_52)
