import os

base_dir = r"c:\Users\Admin\Downloads\INTERNATO GO\site_obstetricia"
comp_dir = os.path.join(base_dir, "components")
index_path = os.path.join(base_dir, "index.html")

with open(index_path, "r", encoding="utf-8") as f:
    index_html = f.read()

comps = [
    "header.html", "hero.html", "modulos-index.html", "modulo-1-leopold.html",
    "calculadoras.html", "modulo-2-ultrassom.html", "modulo-4-imunizacoes.html",
    "modulo-5-dmg-preeclampsia.html", "modulo-6-ctg-doppler.html", "modulo-7-stff.html",
    "modulo-8-rh.html", "modulo-9-10-11-infeccoes.html", "flashcards.html",
    "quiz-simulado.html", "high-yield-summary.html", "footer.html", "modals.html"
]

all_ok = True
for c in comps:
    cp = os.path.join(comp_dir, c)
    with open(cp, "r", encoding="utf-8") as f:
        comp_content = f.read().strip()
    # Check if a signature of the component is in index.html
    sig = comp_content[:80].strip()
    if sig in index_html:
        print(f"Component {c}: MATCHED in index.html")
    else:
        print(f"Component {c}: NOT exact match! Sig: {sig[:40]}")
        all_ok = False

if all_ok:
    print("\nALL 17 COMPONENTS MATCH index.html!")
