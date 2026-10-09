import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fixed widths
fixed_widths = re.findall(r'(w-\[\d+px\]|min-w-\[\d+px\])', html)
print("Fixed/Min width classes found:", set(fixed_widths))

# 2. Check all <table occurrences
table_matches = [m.start() for m in re.finditer(r'<table', html)]
print(f"Total tables: {len(table_matches)}")

tables_unwrapped = []
for idx in table_matches:
    # check preceding 200 chars
    preceding = html[max(0, idx-250):idx]
    if 'overflow-x-auto' not in preceding and 'overflow-auto' not in preceding:
        tables_unwrapped.append(preceding[-100:].strip().replace('\n', ' '))

print(f"Tables possibly without overflow wrapper: {len(tables_unwrapped)}")
for t in tables_unwrapped:
    print("  ->", t)

# 3. Check for grid-cols-[3-9] or grid-cols-12 that don't have sm: or md: preceding or following
grid_matches = re.finditer(r'class=["\'][^"\']*grid-cols-([3-9]|1[0-2])[^"\']*["\']', html)
raw_grids = []
for m in grid_matches:
    s = m.group(0)
    # Check if it has grid-cols-1 or sm: or md:
    if 'grid-cols-1' not in s and 'sm:grid-cols' not in s and 'md:grid-cols' not in s:
        raw_grids.append(s)

print(f"Grids with 3+ columns without mobile fallback: {len(raw_grids)}")
for g in set(raw_grids):
    print("  ->", g[:120])

# 4. Check for nowrap or whitespace-nowrap that might cause overflow
nowraps = re.findall(r'whitespace-nowrap', html)
print("Occurrences of whitespace-nowrap:", len(nowraps))
