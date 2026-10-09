import os
import re

def main():
    base_dir = r"c:\Users\Admin\Downloads\INTERNATO GO"
    index_path = os.path.join(base_dir, "index.html")
    components_dir = os.path.join(base_dir, "components")
    os.makedirs(components_dir, exist_ok=True)

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Define sections by regex or comments
    # Header: <header ... </header>
    header_match = re.search(r'(  <!-- NAVIGATION HEADER -->\s*<header.*?</header>)', content, re.DOTALL)
    if header_match:
        with open(os.path.join(components_dir, "header.html"), "w", encoding="utf-8") as f:
            f.write(header_match.group(1).strip() + "\n")
        print("Created components/header.html")

    # Hero: <!-- HERO SECTION --> ... </section>
    hero_match = re.search(r'(  <!-- HERO SECTION -->\s*<section.*?</section>)', content, re.DOTALL)
    if hero_match:
        with open(os.path.join(components_dir, "hero.html"), "w", encoding="utf-8") as f:
            f.write(hero_match.group(1).strip() + "\n")
        print("Created components/hero.html")

    # Modulos Index: <!-- QUICK NAVIGATION DRAWER / INDEX --> ... </section>
    modulos_index_match = re.search(r'(  <!-- QUICK NAVIGATION DRAWER / INDEX -->\s*<section id="modulos-index".*?</section>)', content, re.DOTALL)
    if modulos_index_match:
        with open(os.path.join(components_dir, "modulos-index.html"), "w", encoding="utf-8") as f:
            f.write(modulos_index_match.group(1).strip() + "\n")
        print("Created components/modulos-index.html")

    # Modulo 1: Leopold
    m1_match = re.search(r'(  <!-- =+ MÓDULO 1 =+ -->\s*<section id="modulo-1".*?</section>)', content, re.DOTALL)
    if not m1_match:
        m1_match = re.search(r'(  <!-- =+ M[^\n]+DULO 1 =+ -->\s*<section id="modulo-1".*?</section>)', content, re.DOTALL)
    if m1_match:
        with open(os.path.join(components_dir, "modulo-1-leopold.html"), "w", encoding="utf-8") as f:
            f.write(m1_match.group(1).strip() + "\n")
        print("Created components/modulo-1-leopold.html")

    # Calculadoras
    calc_match = re.search(r'(  <!-- =+ CALCULADORA NAEGELE & IG =+ -->\s*<section id="calculadoras".*?</section>)', content, re.DOTALL)
    if calc_match:
        with open(os.path.join(components_dir, "calculadoras.html"), "w", encoding="utf-8") as f:
            f.write(calc_match.group(1).strip() + "\n")
        print("Created components/calculadoras.html")

    # Modulo 2: Ultrassom & Rastreamento
    m2_match = re.search(r'(  <!-- =+ M[^\n]+DULO 2 =+ -->\s*<section id="modulo-2".*?</section>)', content, re.DOTALL)
    if m2_match:
        with open(os.path.join(components_dir, "modulo-2-ultrassom.html"), "w", encoding="utf-8") as f:
            f.write(m2_match.group(1).strip() + "\n")
        print("Created components/modulo-2-ultrassom.html")

    # Modulo 4: Imunizações
    m4_match = re.search(r'(  <!-- =+ M[^\n]+DULO 4[^\n]*=+ -->\s*<section id="modulo-4".*?</section>)', content, re.DOTALL)
    if m4_match:
        with open(os.path.join(components_dir, "modulo-4-imunizacoes.html"), "w", encoding="utf-8") as f:
            f.write(m4_match.group(1).strip() + "\n")
        print("Created components/modulo-4-imunizacoes.html")

    # Modulo 5: DMG & Pré-Eclâmpsia
    m5_match = re.search(r'(  <!-- =+ M[^\n]+DULO 5[^\n]*=+ -->\s*<section id="modulo-5".*?</section>)', content, re.DOTALL)
    if m5_match:
        with open(os.path.join(components_dir, "modulo-5-dmg-preeclampsia.html"), "w", encoding="utf-8") as f:
            f.write(m5_match.group(1).strip() + "\n")
        print("Created components/modulo-5-dmg-preeclampsia.html")

    # Modulo 6: Bem-Estar Fetal, CTG & Doppler
    m6_match = re.search(r'(  <!-- =+ M[^\n]+DULO 6[^\n]*=+ -->\s*<section id="modulo-6".*?</section>)', content, re.DOTALL)
    if m6_match:
        with open(os.path.join(components_dir, "modulo-6-ctg-doppler.html"), "w", encoding="utf-8") as f:
            f.write(m6_match.group(1).strip() + "\n")
        print("Created components/modulo-6-ctg-doppler.html")

    # Modulo 7: STFF
    m7_match = re.search(r'(  <!-- =+ M[^\n]+DULO 7[^\n]*=+ -->\s*<section id="modulo-7".*?</section>)', content, re.DOTALL)
    if m7_match:
        with open(os.path.join(components_dir, "modulo-7-stff.html"), "w", encoding="utf-8") as f:
            f.write(m7_match.group(1).strip() + "\n")
        print("Created components/modulo-7-stff.html")

    # Modulo 8: Isoimunização Rh
    m8_match = re.search(r'(  <!-- =+ M[^\n]+DULO 8[^\n]*=+ -->\s*<section id="modulo-8".*?</section>)', content, re.DOTALL)
    if m8_match:
        with open(os.path.join(components_dir, "modulo-8-rh.html"), "w", encoding="utf-8") as f:
            f.write(m8_match.group(1).strip() + "\n")
        print("Created components/modulo-8-rh.html")

    # Modulos 9, 10, 11: Infecções e LA
    m9_match = re.search(r'(  <!-- =+ M[^\n]+DULOS 9, 10 & 11[^\n]*=+ -->\s*<section id="modulo-9".*?</section>)', content, re.DOTALL)
    if m9_match:
        with open(os.path.join(components_dir, "modulo-9-10-11-infeccoes.html"), "w", encoding="utf-8") as f:
            f.write(m9_match.group(1).strip() + "\n")
        print("Created components/modulo-9-10-11-infeccoes.html")

    # Flashcards
    flash_match = re.search(r'(  <!-- =+ FLASHCARDS 3D INTERATIVOS =+ -->\s*<section id="flashcards-section".*?</section>)', content, re.DOTALL)
    if flash_match:
        with open(os.path.join(components_dir, "flashcards.html"), "w", encoding="utf-8") as f:
            f.write(flash_match.group(1).strip() + "\n")
        print("Created components/flashcards.html")

    # Quiz / Simulado
    quiz_match = re.search(r'(  <!-- =+ SIMULADO USMLE STEP 2 CK / STEP 3 =+ -->\s*<section id="quiz-section".*?</section>)', content, re.DOTALL)
    if quiz_match:
        with open(os.path.join(components_dir, "quiz-simulado.html"), "w", encoding="utf-8") as f:
            f.write(quiz_match.group(1).strip() + "\n")
        print("Created components/quiz-simulado.html")

    # High-Yield Summary
    hy_match = re.search(r'(  <!-- =+ HIGH-YIELD REVIEW CHEAT SHEET =+ -->\s*<section id="high-yield-summary".*?</section>)', content, re.DOTALL)
    if hy_match:
        with open(os.path.join(components_dir, "high-yield-summary.html"), "w", encoding="utf-8") as f:
            f.write(hy_match.group(1).strip() + "\n")
        print("Created components/high-yield-summary.html")

    # Footer: <footer ... </footer>
    footer_match = re.search(r'(  <footer.*?</footer>)', content, re.DOTALL)
    if footer_match:
        with open(os.path.join(components_dir, "footer.html"), "w", encoding="utf-8") as f:
            f.write(footer_match.group(1).strip() + "\n")
        print("Created components/footer.html")

    # Modals & Lightbox
    modals_match = re.search(r'(  <!-- =+ MODALS & LIGHTBOXES =+ -->.*?(?=  <!-- Scripts|$))', content, re.DOTALL)
    if modals_match:
        with open(os.path.join(components_dir, "modals.html"), "w", encoding="utf-8") as f:
            f.write(modals_match.group(1).strip() + "\n")
        print("Created components/modals.html")

    print("\nExtraction of components completed successfully!")

if __name__ == "__main__":
    main()
