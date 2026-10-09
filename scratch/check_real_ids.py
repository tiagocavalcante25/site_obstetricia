import re

with open('assets/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract all getElementById strings
js_ids = sorted(list(set(re.findall(r"getElementById\(['\"]([a-zA-Z0-9_\-]+)['\"]\)", js))))

print(f"Total unique getElementById in app.js: {len(js_ids)}")

missing_in_html = []
found_in_html = []

for elem_id in js_ids:
    if f'id="{elem_id}"' in html or f"id='{elem_id}'" in html:
        found_in_html.append(elem_id)
    else:
        missing_in_html.append(elem_id)

print(f"Found in index.html: {len(found_in_html)}")
print(f"Missing in index.html: {len(missing_in_html)}")
for m in missing_in_html:
    print(f"  - {m}")
