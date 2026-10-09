with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '<section id="modulo-5"' in l or '<!-- ==================== MÓDULO 5' in l:
        print(f"M5: line {i+1}: {l.strip()[:80]}")
    if '<section id="modulo-6"' in l or '<!-- ==================== MÓDULO 6' in l:
        print(f"M6: line {i+1}: {l.strip()[:80]}")
